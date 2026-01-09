import { motion } from 'framer-motion';
import { Activity } from 'lucide-react';
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
    CartesianGrid, LineChart, Line, AreaChart, Area, Legend
} from 'recharts';

export const DynamicChart = ({ config }) => {
    if (!config || !config.data) return null;

    const ChartComponent = {
        bar: BarChart,
        line: LineChart,
        area: AreaChart
    }[config.type] || BarChart;

    const DataComponent = {
        bar: Bar,
        line: Line,
        area: Area
    }[config.type] || Bar;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mt-4 mb-6 p-6 rounded-xl bg-slate-800/50 border border-slate-700 backdrop-blur-sm"
        >
            <div className="flex items-center gap-2 mb-6">
                <Activity size={18} className="text-indigo-400" />
                <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">
                    {config.title || "Data Visualization"}
                </h3>
            </div>
            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <ChartComponent data={config.data}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                        <XAxis
                            dataKey={config.xKey}
                            stroke="#94a3b8"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                            dy={10}
                        />
                        <YAxis
                            stroke="#94a3b8"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                            tickFormatter={(value) => `$${value}`}
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }}
                            itemStyle={{ color: '#e2e8f0' }}
                            cursor={{ fill: '#334155', opacity: 0.4 }}
                        />
                        <Legend wrapperStyle={{ paddingTop: '20px' }} />
                        {config.series.map((s, idx) => (
                            <DataComponent
                                key={idx}
                                type="monotone"
                                dataKey={s.dataKey}
                                fill={s.color}
                                stroke={s.color}
                                strokeWidth={3}
                                radius={[4, 4, 0, 0]}
                                activeDot={{ r: 8 }}
                            />
                        ))}
                    </ChartComponent>
                </ResponsiveContainer>
            </div>
        </motion.div>
    );
};