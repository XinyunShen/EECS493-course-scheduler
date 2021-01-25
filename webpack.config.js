const path = require('path');

module.exports = {
  mode: 'development',
  entry: {
    index: './wolfpack/js/main.jsx',
  },
  output: {
    path: path.join(__dirname, '/wolfpack/static/js/'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/preset-react'],
        },
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};
