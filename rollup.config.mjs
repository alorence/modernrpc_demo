import nodeResolve from "@rollup/plugin-node-resolve";

export default {
  input: 'www/index.js',
  output: {
    file: 'dist/app.js',
  },
  plugins: [nodeResolve()]
}
