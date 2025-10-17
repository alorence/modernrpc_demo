import "flyonui/dist/tabs"
import Alpine from 'alpinejs'

import InitApp from "./init.js"

InitApp(function () {
  window.Alpine = Alpine
  Alpine.start()
  console.log("JS initialization is done")
})
