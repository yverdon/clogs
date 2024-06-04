import { defineConfig } from 'vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';

const cesiumSource = 'node_modules/cesium/Build/Cesium';
const cesiumBaseUrl = 'lib/cesium/';

export default defineConfig({
  base: './',
  build: {
    outDir: 'dist/app/',
    sourcemap: true,
    emptyOutDir: true,
  },
  optimizeDeps: {
    include: ['cesium', 'olcs/OLCesium']
  },
  plugins: [
    viteStaticCopy({
      targets: [
        { src: `${cesiumSource}/ThirdParty`, dest: cesiumBaseUrl },
        { src: `${cesiumSource}/Workers`, dest: cesiumBaseUrl },
        { src: `${cesiumSource}/Assets`, dest: cesiumBaseUrl },
        { src: `${cesiumSource}/Widgets`, dest: cesiumBaseUrl },
        { src: 'node_modules/@geogirafe/lib-geoportal/styles/*.css', dest: 'styles/' },
        { src: 'node_modules/@geogirafe/lib-geoportal/public/icons/*', dest: 'icons/' },
        { src: 'node_modules/@geogirafe/lib-geoportal/public/lib/*', dest: 'lib/' },
        { src: 'node_modules/ol/ol.css', dest: 'lib/ol/' },
        { src: 'node_modules/gridjs/dist/theme/mermaid.min.css', dest: 'lib/gridjs/' },
        { src: 'node_modules/font-gis/css/*.css', dest: 'lib/font-gis/' },
        { src: 'node_modules/font-gis/fonts/*', dest: 'lib/fonts/' },
        { src: 'node_modules/tippy.js/dist/*.css', dest: 'lib/tippy.js/' },
        { src: 'node_modules/vanilla-picker/dist/*.css', dest: 'lib/vanilla-picker/' },
        { src: 'config.json', dest: '' }
      ]
    })
  ],
  define: {
    CESIUM_BASE_URL: JSON.stringify(cesiumBaseUrl)
  }
});
