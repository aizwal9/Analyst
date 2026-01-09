import { Bot, User, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { ActionCard } from './ActionCard';
import { DynamicChart } from './DynamicChart';
import { SQLBlock } from './sqlblock';

export const Message = ({ message, onApprove }) => {
    const isBot = message.role === 'assistant';

    return (
        <motion.div
            initial={{ opacity: 0, x: isBot ? -20 : 20 }}
            animate={{ opacity: 1, x: 0 }}
            className={`flex gap-4 mb-8 ${isBot ? 'flex-row' : 'flex-row-reverse'}`}
        >
            {/* Avatar */}
            <div className={`
        w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0
        ${isBot ? 'bg-indigo-500/20 text-indigo-400' : 'bg-slate-700 text-slate-300'}`}>
                {isBot ? <Bot size={20} /> : <User size={20} />}
            </div>

            {/* Content */}
            <div className={`flex flex-col max-w-[80%] ${isBot ? 'items-start' : 'items-end'}`}>

                {/* Text Bubble */}
                {message.content && (
                    <div className={`
            px-5 py-3.5 rounded-2xl text-sm leading-relaxed shadow-sm
            ${isBot
                            ? 'bg-slate-800 text-slate-200 rounded-tl-none border border-slate-700/50'
                            : 'bg-indigo-600 text-white rounded-tr-none shadow-indigo-500/10'}`}>
                        {message.content}
                    </div>
                )}

                {/* Structured Data Components (Only for Bot) */}
                {isBot && (
                    <div className="w-full mt-2 space-y-2">

                        {/* 1. SQL Visualization */}
                        {message.sql_query && (
                            <SQLBlock code={message.sql_query} />
                        )}

                        {/* 2. Chart Visualization */}
                        {message.visualization_spec && (
                            <DynamicChart config={message.visualization_spec} />
                        )}

                        {/* 3. Action Card (Human in the Loop) */}
                        {message.needs_approval && (
                            <ActionCard
                                emailDraft={message.email_draft}
                                threadId={message.thread_id}
                                onAction={onApprove}
                            />
                        )}

                        {/* 4. Steps Indicator */}
                        {message.steps && (
                            <div className="flex gap-2 mt-2">
                                {message.steps.map((step, i) => (
                                    <div key={i} className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700 text-xs text-slate-400">
                                        <Check size={10} className="text-emerald-500" />
                                        {step}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </motion.div>
    );
};
