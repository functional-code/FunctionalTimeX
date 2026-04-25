function AssistantConsole({ assistantMessage, setAssistantMessage, submitAssistant, loading, assistantResult }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl lg:col-span-2">
      <h2 className="mb-3 text-lg font-semibold text-white">AI Assistant Console</h2>
      <form onSubmit={submitAssistant} className="flex flex-col gap-3">
        <textarea
          value={assistantMessage}
          onChange={(e) => setAssistantMessage(e.target.value)}
          placeholder="Example: I need to submit assignment and prep for Monday standup."
          className="min-h-[120px] rounded-xl border border-white/10 bg-slate-900/60 p-4 text-sm text-slate-100 outline-none ring-violet-500 transition focus:ring"
        />
        <button disabled={loading} className="w-fit rounded-xl bg-violet-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-violet-400 disabled:opacity-50">
          {loading ? 'Thinking...' : 'Generate Proactive Plan'}
        </button>
      </form>
      {assistantResult && (
        <div className="mt-4 rounded-xl border border-violet-300/20 bg-violet-700/10 p-4 text-sm">
          <p className="font-medium text-violet-100">{assistantResult.response}</p>
          <p className="mt-2 text-slate-300">
            Intent: <span className="font-semibold text-white">{assistantResult.intent.intent}</span>
          </p>
          <div className="mt-2 flex flex-wrap gap-2">
            {assistantResult.next_actions.map((step) => (
              <span key={step} className="rounded-full border border-violet-300/30 px-3 py-1 text-xs text-violet-100">
                {step}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default AssistantConsole
