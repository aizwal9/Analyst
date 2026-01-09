import { useState } from 'react';
import { Send, Check, X, Loader2, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { Typewriter } from './typewriter';

export const ActionCard = ({ emailDraft, threadId, onAction }) => {
    const [status, setStatus] = useState('pending'); // pending, sending, sent, rejected

    const handleAction = async (approved) => {
        setStatus(approved ? 'sending' : 'rejected');
        try {
            await onAction(threadId, approved);
            setStatus(approved ? 'sent' : 'rejected');
        } catch (e) {
            console.error(e);
            setStatus('pending');
        }
    };

    if (status === 'sent') {
        return (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center gap-3">
                <div className="p-2 rounded-full bg-emerald-500/20 text-emerald-400">
                    <Check size={18} />
                </div>
                <span className="text-emerald-200 font-medium">Email sent successfully.</span>
            </motion.div>
        );
    }

    if (status === 'rejected') {
        return (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center gap-3">
                <div className="p-2 rounded-full bg-red-500/20 text-red-400">
                    <X size={18} />
                </div>
                <span className="text-red-200 font-medium">Action cancelled by user.</span>
            </motion.div>
        );
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-0 rounded-xl overflow-hidden bg-slate-800 border border-indigo-500/30 shadow-2xl shadow-indigo-500/10"
        >
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-3 flex items-center justify-between">
                <div className="flex items-center gap-2 text-white font-medium">
                    <Sparkles size={18} />
                    <span>Human-in-the-Loop Required</span>
                </div>
                <span className="text-xs bg-white/20 text-white px-2 py-1 rounded-full backdrop-blur-md">
                    Action Paused
                </span>
            </div>

            <div className="p-6">
                <div className="text-slate-400 text-xs uppercase tracking-wider font-semibold mb-2">
                    Proposed Email Draft
                </div>
                <div className="bg-slate-900/50 p-4 rounded-lg border border-slate-700 text-slate-300 text-sm whitespace-pre-wrap leading-relaxed font-sans">
                    <Typewriter text={emailDraft} delay={5} />
                </div>

                <div className="flex gap-3 mt-6">
                    <button
                        onClick={() => handleAction(false)}
                        disabled={status === 'sending'}
                        className="flex-1 px-4 py-3 rounded-lg border border-slate-600 text-slate-300 hover:bg-slate-700 transition-colors font-medium flex items-center justify-center gap-2"
                    >
                        <X size={18} />
                        Reject
                    </button>
                    <button
                        onClick={() => handleAction(true)}
                        disabled={status === 'sending'}
                        className="flex-[2] px-4 py-3 rounded-lg bg-indigo-500 hover:bg-indigo-600 text-white transition-all shadow-lg shadow-indigo-500/25 font-medium flex items-center justify-center gap-2"
                    >
                        {status === 'sending' ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} />}
                        Approve & Send
                    </button>
                </div>
            </div>
        </motion.div>
    );
};