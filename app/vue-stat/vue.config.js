//const { RuleTester } = require('eslint');
const path = require('path');

module.exports = {
  // Should be STATIC_URL + path/to/build
  publicPath: '/static/src/vue-userpage/dist/',

  // Output to a directory in STATICFILES_DIRS
  outputDir: path.resolve(__dirname, '../static/src/vue-userpage/dist/'),

  // Django will hash file names, not webpack
  filenameHashing: false,

  runtimeCompiler: true,

  //chainWebpack: config => { 
  //  const types = ['vue-modules', 'vue', 'normal-modules', 'normal']
  // types.forEach(type=> addStyleResource(config.module.rule('styles').oneOf(type)))
  // }
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
//function addStyleResource (rule) { 
  //  rule.use('style-resource')
    //    .loader('style-resources-loader')
      //  .options({ 
        //    patterns: [
          //      path.resolve(__dirname, './src/styles/imports.style'),
          //  ],
       // })
//}
