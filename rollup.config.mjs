import copy from 'rollup-plugin-copy'

export default {
  input: 'www/index.js',
  output: {
    file: 'dist/app.js',
  },
  plugins: [
    copy({
      targets: [
        {
          dest: 'dist/',
          src: [
            // 'node_modules/flyonui/dist/accordion.js',
            'node_modules/flyonui/dist/tabs.js'
          ]
        }
      ]
    })
  ]
}
