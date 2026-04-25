import { useEffect, useState } from 'react'
import { Sparkles } from 'lucide-react'
import AssistantConsole from './components/AssistantConsole'
import TaskQueue from './components/TaskQueue'
import ProductivityChart from './components/ProductivityChart'
import { fetchTasks, parseAssistant } from './services/api'

function App() {
  const [tasks, setTasks] = useState([])
  const [assistantMessage, setAssistantMessage] = useState('')
  const [assistantResult, setAssistantResult] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchTasks().then(setTasks).catch(() => setTasks([]))
  }, [])

  const productivity = [
    { day: 'Mon', score: 52 },
    { day: 'Tue', score: 61 },
    { day: 'Wed', score: 58 },
    { day: 'Thu', score: 72 },
    { day: 'Fri', score: 78 },
    { day: 'Sat', score: 64 },
    { day: 'Sun', score: 81 },
  ]

  const submitAssistant = async (e) => {
    e.preventDefault()
    if (!assistantMessage.trim()) return
    setLoading(true)
    try {
      const result = await parseAssistant(assistantMessage)
      setAssistantResult(result)
      setTasks(await fetchTasks())
      setAssistantMessage('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto min-h-screen w-full max-w-7xl p-6 lg:p-10">
      <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="mb-2 inline-flex items-center gap-2 rounded-full border border-violet-400/30 bg-violet-600/20 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-violet-100">
            <Sparkles className="h-4 w-4" /> FunctionalARIA
          </p>
          <h1 className="text-3xl font-semibold text-white lg:text-4xl">Proactive Intelligence Dashboard</h1>
          <p className="mt-2 text-sm text-slate-300">Anticipate priorities, align schedules, and surface next actions early.</p>
        </div>
        <div className="rounded-xl border border-cyan-300/30 bg-cyan-600/10 px-4 py-3 text-sm text-cyan-100">
          Live Focus Score: <span className="font-bold text-cyan-200">{productivity.at(-1).score}%</span>
        </div>
      </div>

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <AssistantConsole
          assistantMessage={assistantMessage}
          setAssistantMessage={setAssistantMessage}
          submitAssistant={submitAssistant}
          loading={loading}
          assistantResult={assistantResult}
        />
        <TaskQueue tasks={tasks} />
      </section>

      <ProductivityChart productivity={productivity} />
    </main>
  )
}

export default App
