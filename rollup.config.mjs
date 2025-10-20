import nodeResolve from "@rollup/plugin-node-resolve";
import copy from 'rollup-plugin-copy'

export default {
  input: 'www/index.js',
  output: {
    file: 'dist/app.js',
  },
  plugins: [
    nodeResolve(),
    copy({
      verbose: true,
      targets: [
        { src: 'node_modules/clipboard/dist/clipboard.js', dest: 'dist' },
        { src: 'node_modules/flyonui/dist/helper-clipboard.js', dest: 'dist' },
      ]
    })
  ]
}
