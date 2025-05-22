import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools' //
import { createHtmlPlugin } from 'vite-plugin-html'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [
      vue(), //
      vueDevTools(), //
      createHtmlPlugin({
        minify: true,
        inject: {
          data: {
            // VITE_KAKAO_MAP_API_KEY 값을 index.html에서 kakaoApiKey로 사용할 수 있게 전달
            kakaoApiKey: env.VITE_KAKAO_MAP_API_KEY,
          },
        },
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)) //
      }
    }
  }
})