import { motion } from 'framer-motion';
import { Terminal } from 'lucide-react'

export const SQLBlock = ({ code }) => (
    <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mt-4 mb-4 rounded-lg overflow-hidden border border-slate-700 bg-[#1e1e1e] shadow-lg"
    >
        <div className="flex items-center gap-2 px-4 py-2 bg-[#2d2d2d] border-b border-slate-700">
            <Terminal size={14} className="text-emerald-400" />
            <span className="text-xs text-slate-400 font-mono">postgres_analyst.sql</span>
        </div>
        <div className="p-4 overflow-x-auto">
            <pre className="text-sm font-mono text-emerald-300 whitespace-pre-wrap">
                {code}
            </pre>
        </div>
    </motion.div>
);