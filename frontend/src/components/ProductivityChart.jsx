import { CircleCheckBig } from 'lucide-react'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

function ProductivityChart({ productivity }) {
  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl">
      <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold text-white">
        <CircleCheckBig className="h-5 w-5 text-emerald-300" /> Weekly Productivity Trend
      </h2>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={productivity}>
            <defs>
              <linearGradient id="prod" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.9} />
                <stop offset="95%" stopColor="#22d3ee" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="4 4" stroke="#273049" />
            <XAxis dataKey="day" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip />
            <Area type="monotone" dataKey="score" stroke="#c4b5fd" fill="url(#prod)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default ProductivityChart
