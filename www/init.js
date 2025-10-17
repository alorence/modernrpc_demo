const InitApp = fn => {
  console.log(`[InitApp] document.readyState === ${document.readyState}`)
  if (document.readyState === "loading") {
    console.log('[InitApp] ⏳ Schedule initialization on "DOMContentLoaded" event')
    document.addEventListener("DOMContentLoaded", fn);
  } else {
    console.log(`[InitApp] ➞ Call initialization function synchronously`)
    fn();
  }
}

export default InitApp
