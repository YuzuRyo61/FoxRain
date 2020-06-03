var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var VueLoaderPlugin = require('vue-loader/lib/plugin');
var { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    context: __dirname,
    mode: process.env.NODE_ENV,
    entry: {
        main: './cli/main.js'
    },

    output: {
        filename: "[name]-[hash].js",
        path: path.resolve('./static/build/')
    },

    plugins: [
        new BundleTracker({
            path: '.',
            filename: 'webpack-stats.json'
        }),
        new CleanWebpackPlugin({
            verbose: true
        }),
        new VueLoaderPlugin()
    ],

    module: {
        rules: [
            {
                test: /\.js$/,
                loader: 'babel-loader'
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.scss$/,
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader'
                ]
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            url: false,
                            sourceMap: true
                        }
                    }
                ]
            }
        ]
    },

    resolve: {
        extensions: ['.js', '.vue'],
        modules: [
            'node_modules'
        ],
        alias: {
            'vue': path.resolve('./node_modules/vue/dist/vue.js')
        }
    }
}
