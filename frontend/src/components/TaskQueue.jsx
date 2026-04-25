import { CalendarClock } from 'lucide-react'

function TaskQueue({ tasks }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl">
      <h2 className="mb-3 flex items-center gap-2 text-lg font-semibold text-white">
        <CalendarClock className="h-5 w-5 text-cyan-300" /> Execution Queue
      </h2>
      <div className="space-y-2">
        {tasks.slice(0, 6).map((task) => (
          <div key={task.id} className="rounded-xl border border-white/10 bg-slate-900/40 p-3">
            <p className="font-medium text-white">{task.title}</p>
            <p className="text-xs text-slate-300">
              {task.priority} priority • {task.status}
            </p>
          </div>
        ))}
        {!tasks.length && <p className="text-sm text-slate-300">No tasks yet. Use assistant prompt to auto-capture tasks.</p>}
      </div>
    </div>
  )
}

export default TaskQueue
