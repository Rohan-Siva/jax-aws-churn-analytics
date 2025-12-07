import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { PredictionTimeline } from '../types';

interface PredictionChartProps {
    data: PredictionTimeline[];
}

const PredictionChart: React.FC<PredictionChartProps> = ({ data }) => {
    return (
        <div className="card">
            <h3 className="text-xl font-semibold text-white mb-6">Churn Predictions Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis
                        dataKey="date"
                        stroke="#94a3b8"
                        tick={{ fill: '#94a3b8' }}
                    />
                    <YAxis
                        stroke="#94a3b8"
                        tick={{ fill: '#94a3b8' }}
                        domain={[0, 1]}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1e293b',
                            border: '1px solid #334155',
                            borderRadius: '0.5rem'
                        }}
                        labelStyle={{ color: '#e2e8f0' }}
                    />
                    <Legend wrapperStyle={{ color: '#94a3b8' }} />
                    <Line
                        type="monotone"
                        dataKey="avg_churn_probability"
                        stroke="#0ea5e9"
                        strokeWidth={2}
                        dot={{ fill: '#0ea5e9', r: 4 }}
                        activeDot={{ r: 6 }}
                        name="Avg Churn Probability"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default PredictionChart;
