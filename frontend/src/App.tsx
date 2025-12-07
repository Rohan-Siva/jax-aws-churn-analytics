import Dashboard from './components/Dashboard'

function App() {
    return (
        <div className="min-h-screen bg-slate-900">
            <header className="bg-slate-800 border-b border-slate-700 shadow-lg">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-white">
                                ML Analytics Dashboard
                            </h1>
                            <p className="text-slate-400 mt-1">
                                Real-time churn prediction powered by JAX
                            </p>
                        </div>
                        <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                                <span className="text-sm text-slate-400">Live</span>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Dashboard />
            </main>

            <footer className="bg-slate-800 border-t border-slate-700 mt-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <p className="text-center text-slate-400 text-sm">
                        Built with JAX, FastAPI, PostgreSQL, and React
                    </p>
                </div>
            </footer>
        </div>
    )
}

export default App
