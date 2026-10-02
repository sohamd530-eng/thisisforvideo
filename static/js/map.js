/**
 * SurakshaTaap Pune - Leaflet GIS Spatial Engine for Pune Municipal Corporation (PMC)
 */

let mapInstance = null;
let geojsonLayer = null;
let markersLayerGroup = null;
let currentMetricMode = "wbgt"; // "wbgt", "utci", "hmri", "heat_index"

function initGISMap(lat = 18.5204, lon = 73.8567, zoom = 12) {
    if (mapInstance) {
        mapInstance.remove();
    }

    mapInstance = L.map('map', {
        center: [lat, lon],
        zoom: zoom,
        zoomControl: true
    });

    // Dark high-contrast carto basemap
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a> | MoES, NCMRWF & PMC Pune',
        maxZoom: 19,
        subdomains: 'abcd'
    }).addTo(mapInstance);

    markersLayerGroup = L.layerGroup().addTo(mapInstance);

    return mapInstance;
}

function getChoroplethColor(feature, metric) {
    const p = feature.properties;
    
    if (metric === "hmri") {
        const val = p.hmri_score;
        if (val >= 88) return '#a855f7'; // Purple (Extreme)
        if (val >= 70) return '#ef4444'; // Red (Severe)
        if (val >= 45) return '#f97316'; // Orange (High)
        if (val >= 20) return '#f59e0b'; // Yellow (Moderate)
        return '#10b981'; // Green (Low)
    } else if (metric === "wbgt") {
        const val = p.wbgt_c;
        if (val >= 32.2) return '#a855f7';
        if (val >= 30.0) return '#ef4444';
        if (val >= 28.0) return '#f97316';
        if (val >= 26.0) return '#f59e0b';
        return '#10b981';
    } else if (metric === "utci") {
        const val = p.utci_c;
        if (val >= 46.0) return '#a855f7';
        if (val >= 38.0) return '#ef4444';
        if (val >= 32.0) return '#f97316';
        if (val >= 26.0) return '#f59e0b';
        return '#10b981';
    } else { // heat_index
        const val = p.heat_index_c;
        if (val >= 54.0) return '#a855f7';
        if (val >= 41.0) return '#ef4444';
        if (val >= 32.0) return '#f97316';
        return '#10b981';
    }
}

function renderGeoJSONWards(geojsonData, onWardSelectCallback) {
    if (!mapInstance) return;

    if (geojsonLayer) {
        mapInstance.removeLayer(geojsonLayer);
    }
    if (markersLayerGroup) {
        markersLayerGroup.clearLayers();
    }

    geojsonLayer = L.geoJSON(geojsonData, {
        style: function (feature) {
            const fillColor = getChoroplethColor(feature, currentMetricMode);
            return {
                fillColor: fillColor,
                weight: 2.2,
                opacity: 0.95,
                color: '#334155',
                fillOpacity: 0.62
            };
        },
        onEachFeature: function (feature, layer) {
            const p = feature.properties;
            
            layer.on({
                mouseover: function (e) {
                    const l = e.target;
                    l.setStyle({
                        weight: 3.5,
                        color: '#38bdf8',
                        fillOpacity: 0.85
                    });
                    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                        l.bringToFront();
                    }
                },
                mouseout: function (e) {
                    geojsonLayer.resetStyle(e.target);
                },
                click: function (e) {
                    if (onWardSelectCallback) {
                        onWardSelectCallback(p);
                    }
                }
            });

            // Rich Tooltip with Pune specific attributes
            const tooltipHtml = `
                <div class="p-3 text-xs font-sans">
                    <div class="flex items-center justify-between gap-2 border-b border-slate-700 pb-1.5 mb-2">
                        <div class="font-extrabold text-sm text-sky-400">${p.ward_name}</div>
                        <span class="text-[10px] font-bold px-1.5 py-0.5 rounded" style="background-color:${p.color_code}22; color:${p.color_code}; border: 1px solid ${p.color_code}44;">
                            ${p.risk_tier.split(' ')[0]}
                        </span>
                    </div>
                    <div class="text-[11px] text-slate-300 font-medium mb-1.5">${p.marathi_name}</div>
                    <div class="grid grid-cols-2 gap-x-3 gap-y-1.5">
                        <div><span class="text-slate-400">WBGT Stress:</span> <span class="font-bold text-white">${p.wbgt_c}°C</span></div>
                        <div><span class="text-slate-400">UTCI Human:</span> <span class="font-bold text-white">${p.utci_c}°C</span></div>
                        <div><span class="text-slate-400">HMRI Score:</span> <span class="font-bold text-amber-400">${p.hmri_score}/100</span></div>
                        <div><span class="text-slate-400">UHI Anomaly:</span> <span class="font-bold text-rose-400">+${p.uhi_intensity_c}°C</span></div>
                        <div><span class="text-slate-400">Elderly (>60y):</span> <span class="text-slate-200">${p.elderly_pct}%</span></div>
                        <div><span class="text-slate-400">Tin/Slum Roof:</span> <span class="text-slate-200">${p.slum_density_pct}%</span></div>
                    </div>
                    <div class="mt-2.5 pt-2 border-t border-slate-700/80 flex items-center justify-between text-[11px]">
                        <span class="text-slate-400">Proj. Heatstroke Cases:</span>
                        <span class="font-bold text-red-400">${p.heat_er_admissions_daily} / day</span>
                    </div>
                </div>
            `;
            layer.bindTooltip(tooltipHtml, {
                sticky: true,
                className: 'custom-popup'
            });

            // Add Ward Label marker at centroid
            if (p.centroid && p.centroid.length === 2) {
                const labelIcon = L.divIcon({
                    className: 'ward-badge-pill-container',
                    html: `<div class="ward-badge-pill">${p.ward_name.split(' - ')[0]}</div>`,
                    iconSize: [60, 20],
                    iconAnchor: [30, 10]
                });
                L.marker(p.centroid, { icon: labelIcon }).addTo(markersLayerGroup);
            }
        }
    }).addTo(mapInstance);

    // Fit map bounds to polygons
    try {
        const bounds = geojsonLayer.getBounds();
        if (bounds.isValid()) {
            mapInstance.fitBounds(bounds, { padding: [15, 15] });
        }
    } catch (e) {
        console.error("Bounds error", e);
    }
}

function setChoroplethMetric(metricName, geojsonData, callback) {
    currentMetricMode = metricName;
    if (geojsonData) {
        renderGeoJSONWards(geojsonData, callback);
    }
}
