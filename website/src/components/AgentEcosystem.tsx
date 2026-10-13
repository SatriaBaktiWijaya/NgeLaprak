import React from 'react'
import StackIcon from 'tech-stack-icons'
import type { IconName } from 'tech-stack-icons'

interface ToolItem {
  iconName: IconName
  label: string
}

export const AgentEcosystem: React.FC = () => {
  const tools: ToolItem[] = [
    { iconName: 'antigravity', label: 'Antigravity' },
    { iconName: 'claude', label: 'Claude Code' },
    { iconName: 'cursor', label: 'Cursor' },
    { iconName: 'openai', label: 'OpenAI Codex' },
    { iconName: 'copilotgithub', label: 'GitHub Copilot' },
    { iconName: 'gemini', label: 'Gemini CLI' },
    { iconName: 'vscode', label: 'VS Code' }
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
                key={`${item.iconName}-${idx}`}
                className="flex items-center gap-3 px-6 sm:px-8 shrink-0 group opacity-50 hover:opacity-100 grayscale hover:grayscale-0 transition-all duration-300 cursor-pointer"
              >
                <div className="w-6 h-6 sm:w-7 sm:h-7 shrink-0 transition-transform duration-300 group-hover:scale-110 flex items-center justify-center">
                  <StackIcon
                    name={item.iconName}
                    variant="dark"
                    className="w-full h-full block"
                  />
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
