Ext.define("toto.view.Main", {
    extend: 'Ext.Container',
    requires: [
        'Ext.field.Search',
        'Ext.field.Select',
        'toto.model.Layer',
        'Ext.util.Geolocation'
    ],

    config: {
        map: null,
        layout: 'fit',
        items: [{
            xtype: 'toolbar',
            docked: 'top',
            items: [{
                xtype: 'searchfield',
                flex: 4,
                locales: {
                    placeHolder: 'views.map.search'
                },
                action: 'search'
            }, {
                xtype: 'spacer'
            }, {
                xtype: 'button',
                iconCls: 'settings',
                action: 'settings',
                align: 'right',
                iconMask: true
            }]
        }, {
            id: 'map-container'
        }, {
            xtype: 'button',
            cls: 'zoomin',
            iconCls: 'add',
            action: 'zoomin',
            iconMask: true,
            top: 51,
            left: 10
        }, {
            xtype: 'button',
            cls: 'zoomout',
            iconCls: 'minus1',
            action: 'zoomout',
            iconMask: true,
            top: 85,
            left: 10
        }, {
            xtype: 'button',
            iconCls: 'locate',
            action: 'locate',
            align: 'right',
            iconMask: true,
            top: 10,
            left: 10
        }, {
            xtype: 'selectfield',
            id: 'baselayer_switcher',
            width: 170,
            top: 10,
            right: 10,
            displayField: 'name',
            valueField: 'id'
        }]
    },

    initialize: function() {
        this.callParent(arguments);

        this.on('painted', this.render, this, {
            single: true
        });

        // create the map
        var map = new OpenLayers.Map({
            theme: null,
            layers: [
                new OpenLayers.Layer.OSM(),
                new OpenLayers.Layer.OSM(
                    "Cycle Map",
                    [
                        "http://a.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
                        "http://b.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
                        "http://c.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png"
                    ]
                ),
                new OpenLayers.Layer.OSM(
                    "Transport Map",
                    [
                        "http://a.tile2.opencyclemap.org/transport/${z}/${x}/${y}.png",
                        "http://b.tile2.opencyclemap.org/transport/${z}/${x}/${y}.png",
                        "http://c.tile2.opencyclemap.org/transport/${z}/${x}/${y}.png"
                    ]
                )
            ]
        });
        this.setMap(map);

        // base layer manager
        var baseLayersStore = Ext.create('Ext.data.Store', {
            model: 'toto.model.Layer'
        });
        Ext.each(this.getMap().layers, function(layer) {
            if (layer.isBaseLayer) {
                baseLayersStore.add(layer);
            }
        });
        var baseLayerSwitcher = this.down('#baselayer_switcher');
        baseLayerSwitcher.setStore(baseLayersStore);
        baseLayerSwitcher.on(
            'change',
            function(select, newValue) {
                map.setBaseLayer(map.getLayer(newValue));
            }
        );

        // zoom buttons
        this.down('[action=zoomin]').on('tap', function() {map.zoomIn();});
        this.down('[action=zoomout]').on('tap', function() {map.zoomOut();});

        var geolocation = Ext.create('Ext.util.Geolocation', {
            autoUpdate: false
        });
        this.down('[action=locate]').on(
            'tap',
            function() {
                geolocation.on('locationupdate', function(geo) {
                    var lonlat = new OpenLayers.LonLat(geo.getLongitude(),
                                                       geo.getLatitude());
                    lonlat.transform('EPSG:4326', map.getProjection());
                    map.setCenter(lonlat, 10);
                }, null, {single: true});
                geolocation.updateLocation();
            }
        );
    },

    destroy: function() {
        var map = this.getMap();
        if (map) {
            map.destroy();
        }
        this.callParent();
    },

    // initial rendering
    render: function(component) {
        var map = this.getMap();
        map.render(this.down('#map-container').element.dom);
        map.zoomToMaxExtent();
    }
});
