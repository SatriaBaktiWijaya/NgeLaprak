import React from 'react'

interface ToolItem {
  id: string
  label: string
  icon: React.ReactNode
}

export const AgentEcosystem: React.FC = () => {
  const tools: ToolItem[] = [
    {
      id: 'antigravity',
      label: 'Antigravity',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 100 100" className="w-full h-full block">
          <mask id="ag-mask" width="100" height="93" x="0" y="4" maskUnits="userSpaceOnUse" style={{ maskType: 'alpha' }}>
            <path fill="#fff" d="M90.63 94.027c5.583 4.187 13.958 1.396 6.281-6.28C73.881 65.413 78.766 4 50.153 4S26.425 65.414 3.395 87.746c-8.375 8.375.697 10.468 6.28 6.281C31.31 79.371 29.916 53.55 50.154 53.55S68.996 79.372 90.63 94.027" />
          </mask>
          <g mask="url(#ag-mask)">
            <rect width="100" height="100" fill="url(#ag-grad)" />
          </g>
          <defs>
            <linearGradient id="ag-grad" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#4285F4" />
              <stop offset="35%" stopColor="#34A853" />
              <stop offset="70%" stopColor="#FBBC05" />
              <stop offset="100%" stopColor="#EA4335" />
            </linearGradient>
          </defs>
        </svg>
      )
    },
    {
      id: 'claude',
      label: 'Claude Code',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 100 100" className="w-full h-full block">
          <path fill="#d97757" d="m95.815 38.848 3.465 1.98v1.486l-.99 3.465-42.08 9.901-3.956-9.83z" />
          <path fill="#d97757" d="m80.076 9.73 4.845 1.016 1.286 1.585 1.226 3.799-.508 2.422-28.239 38.613-9.406-9.406 26.04-34.17z" />
          <path fill="#d97757" d="m55.716 3.7 2.97-1.98 2.475.99 2.475 3.465-6.78 40.755-4.605-3.131-1.98-5.446L53.736 7.66z" />
          <path fill="#d97757" d="M23.959 4.352 27.01.454 29 0l3.95.577 1.949 1.526L49.102 33.59l5.137 14.961-6.01 3.342L25.32 10.322z" />
          <path fill="#d97757" d="m9.18 25.979-.99-3.962 2.972-3.465 3.465.495h.99L36.41 34.393l6.435 4.95 8.911 6.931-4.95 8.416-4.455-3.465-2.97-2.97-28.714-20.298z" />
          <path fill="#d97757" d="M3.24 51.72 1 49.244v-2.202l2.24-.768 25.248 1.485 24.753 1.98-.804 4.93-47.216-2.454z" />
          <path fill="#d97757" d="M18.092 77.488h-4.95l-1.968-2.266v-2.71l8.404-5.94 34.166-21.75 3.458 5.907z" />
          <path fill="#d97757" d="m27.498 91.324-1.98.495-2.97-1.486.495-2.475 29.208-38.614 3.96 5.446L34.43 83.403z" />
          <path fill="#d97757" d="m52.25 96.274-1.485 1.98-2.97.99-2.475-1.98-1.486-2.97 7.426-40.1 4.456.496z" />
          <path fill="#d97757" d="M77.499 85.383v3.96l-.495 1.485-1.98.99-3.466-.46-23.796-35.416 9.439-7.193 7.92 14.357.744 5.197z" />
          <path fill="#d97757" d="m88.885 79.442.495 2.475-1.485 1.98-1.485-.495-8.416-5.94-12.871-11.387-9.901-6.93 2.97-9.406 4.95 2.97 2.97 5.445z" />
          <path fill="#d97757" d="m82.448 54.195 12.377.99 2.97 1.98 1.98 2.97v2.138L94.33 64.59l-27.723-6.93-11.386-.496 2.97-10.396 7.921 5.94z" />
        </svg>
      )
    },
    {
      id: 'cursor',
      label: 'Cursor',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 100 100" className="w-full h-full block">
          <path fill="url(#cursor-b)" d="m50 100.136 43.437-25-43.437-25-43.438 25z" />
          <path fill="url(#cursor-c)" d="M93.438 75.137v-50L50 .136v50z" />
          <path fill="url(#cursor-d)" d="m50 .137-43.438 25v50l43.438-25z" />
          <path fill="#c3c3c3" d="m93.438 25.137-43.437 75v-50z" />
          <path fill="#fff" d="M93.437 25.137 50 50.137l-43.438-25z" />
          <defs>
            <linearGradient id="cursor-b" x1="50" x2="50" y1="50.136" y2="100.136" gradientUnits="userSpaceOnUse">
              <stop offset=".16" stopColor="#fff" stopOpacity=".39" />
              <stop offset=".658" stopColor="#fff" stopOpacity=".8" />
            </linearGradient>
            <linearGradient id="cursor-c" x1="93.438" x2="50.001" y1="25.291" y2="50.761" gradientUnits="userSpaceOnUse">
              <stop offset=".182" stopColor="#fff" stopOpacity=".31" />
              <stop offset=".715" stopColor="#fff" stopOpacity="0" />
            </linearGradient>
            <linearGradient id="cursor-d" x1="50" x2="6.562" y1=".137" y2="75.136" gradientUnits="userSpaceOnUse">
              <stop stopColor="#fff" stopOpacity=".6" />
              <stop offset=".667" stopColor="#fff" stopOpacity=".22" />
            </linearGradient>
          </defs>
        </svg>
      )
    },
    {
      id: 'openai',
      label: 'OpenAI Codex',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 100 100" className="w-full h-full block">
          <path fill="#fff" d="M93.06 40.937c1.25-3.438 1.563-6.875 1.25-10.313-.312-3.437-1.562-6.875-3.125-10-2.812-4.687-6.875-8.437-11.562-10.625-5-2.187-10.313-2.812-15.625-1.562-2.5-2.5-5.313-4.688-8.438-6.25S48.685-.001 45.248-.001c-5.313 0-10.625 1.563-15 4.688a24.16 24.16 0 0 0-9.063 12.5c-3.75.937-6.875 2.5-10 4.374-2.812 2.188-5 5-6.875 7.813-2.812 4.688-3.75 10-3.125 15.313a27.2 27.2 0 0 0 6.25 14.375c-1.25 3.437-1.562 6.874-1.25 10.312s1.563 6.875 3.125 10c2.813 4.688 6.875 8.438 11.563 10.625 5 2.188 10.312 2.813 15.625 1.563 2.5 2.5 5.312 4.687 8.437 6.25s6.875 2.187 10.313 2.187c5.312 0 10.625-1.562 15-4.687s7.5-7.5 9.062-12.5c3.438-.626 6.875-2.188 9.688-4.376 2.812-2.187 5.312-4.687 6.875-7.812 2.812-4.687 3.75-10 3.125-15.312-.625-5.313-2.5-10.313-5.938-14.375m-37.5 52.5c-5 0-8.75-1.563-12.187-4.376 0 0 .312-.312.625-.312l20-11.562c.625-.313.937-.626 1.25-1.25.312-.626.312-.938.312-1.563V46.249l8.438 5v23.125c.312 10.938-8.438 19.063-18.438 19.063M15.248 76.249c-2.188-3.75-3.125-8.125-2.188-12.5 0 0 .313.312.625.312l20 11.563c.625.313.938.313 1.563.313s1.25 0 1.562-.313l24.375-14.062v9.687L40.873 83.124c-4.375 2.5-9.375 3.125-14.063 1.875-5-1.25-9.062-4.375-11.562-8.75M9.935 32.812c2.188-3.75 5.625-6.563 9.688-8.125v23.75c0 .625 0 1.25.312 1.562.313.625.625.938 1.25 1.25L45.56 65.311l-8.437 5-20-11.562c-4.375-2.5-7.5-6.562-8.75-11.25s-.938-10.312 1.562-14.687m69.063 15.937L54.623 34.687l8.437-5 20 11.562c3.125 1.875 5.625 4.375 7.188 7.5s2.5 6.563 2.187 10.313c-.312 3.437-1.562 6.874-3.75 9.687s-5 5-8.437 6.25v-23.75c0-.625 0-1.25-.313-1.562 0 0-.312-.625-.937-.938m8.437-12.5s-.312-.312-.625-.312l-20-11.563c-.625-.312-.937-.312-1.562-.312s-1.25 0-1.563.312L39.31 38.437v-9.688l20.313-11.875c3.125-1.875 6.562-2.5 10.312-2.5 3.438 0 6.875 1.25 10 3.437 2.813 2.188 5.313 5 6.563 8.125s1.562 6.876.937 10.313m-52.5 17.5-8.437-5V25.311c0-3.437.937-7.187 2.812-10 1.875-3.124 4.688-5.312 7.813-6.874 3.125-1.563 6.875-2.188 10.312-1.563 3.438.313 6.875 1.875 9.688 4.063 0 0-.313.312-.625.312l-20 11.562c-.625.313-.938.625-1.25 1.25s-.313.938-.313 1.563zm4.375-10 10.938-6.25 10.937 6.25v12.5l-10.937 6.25-10.938-6.25z" />
        </svg>
      )
    },
    {
      id: 'copilotgithub',
      label: 'GitHub Copilot',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 100 100" className="w-full h-full block">
          <path fill="#fff" d="M35.417 60.982a4.066 4.066 0 0 1 8.131 0v7.494a4.066 4.066 0 1 1-8.132 0zm24.899-4.065a4.066 4.066 0 0 0-4.066 4.065v7.494a4.066 4.066 0 1 0 8.132 0v-7.494a4.066 4.066 0 0 0-4.066-4.065" />
          <path fill="#fff" fillRule="evenodd" d="M100 68.331V57.125a6.85 6.85 0 0 0-1.344-4.081l-3.044-4.125c-1.629-2.22-4.042-2.794-6.63-2.794C88.005 35 85.693 27.063 80.187 21.25 69.688 10.125 55.75 9 50 9s-19.687 1.125-30.187 12.25C14.3 27.063 11.993 35 11.019 46.125c-2.583 0-5.008.584-6.638 2.794l-3.043 4.119A6.9 6.9 0 0 0 0 57.125v11.206a4.67 4.67 0 0 0 1.888 3.713C11.645 79.206 30.834 90.25 50 90.25c17.324 0 34.33-8.116 48.113-18.206A4.67 4.67 0 0 0 100 68.33M76.563 47.77c2.156.708 4.228 1.71 4.362 4.262h-.006c.343 7.188.443 14.412.319 21.607a3.66 3.66 0 0 1-2.126 3.274C68.776 81.625 58.995 84 50.006 84c-9 0-18.781-2.375-29.125-7.088a3.66 3.66 0 0 1-2.125-3.275c.035-2.326.046-4.651.055-6.976l.002-.245c.02-4.795.04-9.588.268-14.385.137-2.538 2.2-3.556 4.35-4.262 2.272 1.433 5.056 1.987 7.713 1.987 2.825 0 8.1-.675 12.475-5.05 1.106-1.1 1.862-2.825 2.375-4.737a42 42 0 0 1 4.012-.213q2.005.01 4 .213c.513 1.912 1.269 3.637 2.375 4.737 4.382 4.375 9.65 5.05 12.475 5.05 2.657 0 5.433-.56 7.707-1.987m-47.25-2.956c-3.438 0-6.625-1.126-8.313-2.813-2.312-2.375-3.187-13.625.875-18.062 1.875-2 5.563-3.438 9.938-3.875 4.125-.375 7.812.25 9.437 1.687 1.5 1.25 2.5 4.188 2.625 7.75.125 4.438-1 8.813-2.812 10.563-4.126 4.187-9.126 4.75-11.75 4.75m17.437-11.5c-.062-.813-.125-1.563-.25-2.25 1.313-.125 2.5-.188 3.5-.188s2.188.063 3.5.188c-.125.687-.187 1.437-.25 2.25 0 .562 0 1.124.063 1.75-1.25-.126-2.313-.126-3.313-.126s-2.062 0-3.312.126c.062-.626.062-1.188.062-1.75m12.188 6.75C57.125 38.313 56 33.937 56.125 29.5c.125-3.562 1.125-6.5 2.625-7.75 1.625-1.437 5.313-2.062 9.438-1.687 4.374.437 8.062 1.875 9.937 3.875C82.188 28.375 81.313 39.625 79 42c-1.687 1.688-4.875 2.813-8.312 2.813-2.626 0-7.626-.563-11.75-4.75" clipRule="evenodd" />
        </svg>
      )
    },
    {
      id: 'gemini',
      label: 'Gemini CLI',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 100 100" className="w-full h-full block">
          <path
            fill="url(#gemini-grad)"
            d="M89.165 44.705c-7.705-3.319-14.443-7.864-20.228-13.642-5.778-5.779-10.329-12.523-13.641-20.228a60.4 60.4 0 0 1-3.08-9.102A2.285 2.285 0 0 0 50 0c-1.051 0-1.96.716-2.216 1.733a60 60 0 0 1-3.08 9.102q-4.975 11.56-13.641 20.228c-5.779 5.772-12.523 10.323-20.228 13.642a60.4 60.4 0 0 1-9.102 3.08A2.285 2.285 0 0 0 0 50c0 1.051.716 1.96 1.733 2.216a60 60 0 0 1 9.102 3.08c7.705 3.318 14.443 7.863 20.228 13.642 5.778 5.778 10.329 12.522 13.642 20.227a60 60 0 0 1 3.08 9.102A2.29 2.29 0 0 0 50 100c1.051 0 1.96-.716 2.216-1.733a60 60 0 0 1 3.08-9.102c3.318-7.705 7.863-14.443 13.642-20.228 5.778-5.778 12.522-10.329 20.227-13.641a60 60 0 0 1 9.102-3.08A2.29 2.29 0 0 0 100 50c0-1.051-.716-1.96-1.733-2.216a60 60 0 0 1-9.102-3.08"
          />
          <defs>
            <linearGradient id="gemini-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#4A88F6" />
              <stop offset="45%" stopColor="#9B72CF" />
              <stop offset="100%" stopColor="#D96570" />
            </linearGradient>
          </defs>
        </svg>
      )
    },
    {
      id: 'vscode',
      label: 'VS Code',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 100 100" className="w-full h-full block">
          <path fill="#2489ca" d="M.951 35.498s-2.435-1.756.488-4.1l6.81-6.089s1.948-2.05 4.008-.264l62.839 47.576v22.814s-.03 3.582-4.628 3.186z" />
          <path fill="#1070b3" d="M17.148 50.204.951 64.929s-1.664 1.238 0 3.45l7.52 6.84s1.787 1.919 4.425-.263l17.171-13.02z" />
          <path fill="#0877b9" d="M45.584 50.325 75.29 27.643l-.193-22.692S73.827 0 69.596 2.577L30.067 38.553z" />
          <path fill="#3c99d4" d="M70.469 98.652c1.725 1.766 3.815 1.188 3.815 1.188l23.149-11.407c2.963-2.02 2.547-4.526 2.547-4.526V15.79c0-2.994-3.065-4.029-3.065-4.029L76.852 2.09c-4.384-2.71-7.256.487-7.256.487s3.694-2.659 5.5 2.375v90.067c0 .62-.132 1.228-.396 1.776-.527 1.066-1.674 2.06-4.424 1.644z" />
        </svg>
      )
    }
  ]

  // Duplicate list twice to ensure perfectly seamless, infinite marquee loop
  const carouselItems = [...tools, ...tools, ...tools]

  return (
    <section id="ecosystem" className="relative py-12 md:py-16 border-y border-white/[0.06] bg-[#07080D]/70 backdrop-blur-sm overflow-hidden select-none">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10">
        {/* Minimalist Centered Caption - Just like reference proof bar */}
        <div className="text-center mb-8 sm:mb-10">
          <p className="text-[11px] sm:text-xs font-mono font-medium tracking-[0.24em] uppercase text-slate-400/90">
            Bekerja Mulus di AI Coding Agent Favoritmu:
          </p>
        </div>

        {/* Carousel Container with Left & Right Gradient Fade Masks */}
        <div className="relative w-full overflow-hidden">
          {/* Left Gradient Fade Mask */}
          <div className="pointer-events-none absolute left-0 top-0 bottom-0 w-16 sm:w-28 bg-gradient-to-r from-[#07080D] via-[#07080D]/80 to-transparent z-10" />

          {/* Right Gradient Fade Mask */}
          <div className="pointer-events-none absolute right-0 top-0 bottom-0 w-16 sm:w-28 bg-gradient-to-l from-[#07080D] via-[#07080D]/80 to-transparent z-10" />

          {/* Infinite Marquee Ticker */}
          <div className="animate-marquee py-2 flex items-center">
            {carouselItems.map((item, idx) => (
              <div
                key={`${item.id}-${idx}`}
                className="flex items-center gap-3 px-6 sm:px-8 shrink-0 group opacity-50 hover:opacity-100 grayscale hover:grayscale-0 transition-all duration-300 cursor-pointer"
              >
                <div className="w-6 h-6 sm:w-7 sm:h-7 shrink-0 transition-transform duration-300 group-hover:scale-110 flex items-center justify-center">
                  {item.icon}
                </div>
                <span className="text-xs sm:text-sm font-semibold tracking-tight text-slate-400 group-hover:text-white transition-colors duration-200 whitespace-nowrap">
                  {item.label}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
