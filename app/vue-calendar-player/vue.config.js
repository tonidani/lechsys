const path = require('path');

module.exports = {
    // Should be STATIC_URL + path/to/build
    publicPath: '/static/src/vue-calendar-player/dist/',

    // Output to a directory in STATICFILES_DIRS
    outputDir: path.resolve(__dirname, '../static/src/vue-calendar-player/dist/'),

    // Django will hash file names, not webpack
    filenameHashing: false,

    runtimeCompiler: true,

    devServer: {
        writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
    },

    pluginOptions: {
      i18n: {
        locale: 'en',
        fallbackLocale: 'en',
        localeDir: 'locales',
        enableInSFC: false,
        enableBridge: false
      }
    }
};
