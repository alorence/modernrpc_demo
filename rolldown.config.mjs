import { copyFile, mkdir } from 'node:fs/promises'
import { basename, join } from 'node:path'
import { defineConfig } from 'rolldown'

/**
 * Copy standalone vendor scripts to the output directory
 */
function copyVendorFiles(files, dest) {
  return {
    name: 'copy-vendor-files',
    async writeBundle() {
      await mkdir(dest, { recursive: true })
      await Promise.all(files.map((src) => copyFile(src, join(dest, basename(src)))))
    },
  }
}

export default defineConfig({
  input: 'www/index.js',
  output: {
    file: 'dist/app.js',
  },
  plugins: [
    copyVendorFiles(
      [
        'node_modules/clipboard/dist/clipboard.js',
        'node_modules/flyonui/dist/helper-clipboard.js',
      ],
      'dist',
    ),
  ],
})
