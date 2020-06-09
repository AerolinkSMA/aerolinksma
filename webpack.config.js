const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const devMode = process.env.NODE_ENV !== 'production';

module.exports = {
  entry: './aerolinksma/assets/js/main.js',
  mode: devMode ? 'development' : 'production',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'aerolinksma', 'static', 'js'),
  },
  plugins: [
    new CleanWebpackPlugin({ cleanStaleWebpackAssets: false }),
  ],
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          'style-loader', // inject CSS to page
          'css-loader', // translates CSS into CommonJS modules
          {
            loader: 'postcss-loader', // run postcss actions
            options: {
              plugins: function () {
                return [
                  require('autoprefixer')
                ];
              }
            }
          },
          'sass-loader', // compiles Sass to CSS
        ],
      },
    ],
  },
};
