# Getting Started

### Install dependencies

```
npm install
```

### Start the development server

```
npm start
```

### Build for production

```
npm run build
```

### Preview production

```
npm run preview
```

### Update to last version of GeoGirafe

```
npm update @geogirafe/lib-geoportal
```

# Configure and customize your instance

### Main configuration

The file `config.json` contains the application configuration.  
See https://doc.geomapfish.dev/docs/configuration for more configuration options.

### Themes and layers

The file `public/mock/themes.json` contains the themes configuration.  
Consult the GeoMapFish documentation for more infos about this, or have a look at the demos for some examples :
  - https://demo.geomapfish.dev/mapbs/Mock/themes.json
  - https://demo.geomapfish.dev/sitn/Mock/themes.json
  - https://demo.geomapfish.dev/mapnv/Mock/themes.json

### Translations

The file `public/mock/en.json` contains the application translations.

### Main interface

The file `index.html` defines your application template.  
A complete example can be found here: https://gitlab.com/geogirafe/gg-viewer/-/blob/main/index.html?ref_type=heads

### Styling

The file `custom.css` ist the way were custom css can be placed.

# Develop your own components

### Your first custom component

The directory `src/components/my-first-component` contains an example on how to create a custom component for GeoGirafe.

### Extending an existing component

The directory `src/components/my-extended-component` contains an example on how to extend an existing component.

# Contact

You can join our Discord server at any time to get some help or just to discuss with us: https://discord.gg/kdrXjaqBbH.

_Have a nice journey with GeoGirafe ! :-)_
