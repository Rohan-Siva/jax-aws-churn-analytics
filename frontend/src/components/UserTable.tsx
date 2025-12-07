import React from 'react';
import type { UserAnalytics } from '../types';

interface UserTableProps {
    users: UserAnalytics[];
}

const UserTable: React.FC<UserTableProps> = ({ users }) => {
    const getRiskLevel = (prediction: number | null): { label: string; color: string } => {
        if (prediction === null) return { label: 'Unknown', color: 'text-slate-400' };
        if (prediction >= 0.7) return { label: 'High', color: 'text-red-400' };
        if (prediction >= 0.4) return { label: 'Medium', color: 'text-yellow-400' };
        return { label: 'Low', color: 'text-green-400' };
    };

    return (
        <div className="card">
            <h3 className="text-xl font-semibold text-white mb-6">User Churn Risk</h3>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-700">
                    <thead>
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                                Email
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                                Tier
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                                Events
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                                Last Active
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                                Churn Risk
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                                Status
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700">
                        {users.map((user) => {
                            const risk = getRiskLevel(user.latest_churn_prediction);
                            return (
                                <tr key={user.user_id} className="hover:bg-slate-700/50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-white">
                                        {user.email}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                                        <span className="px-2 py-1 text-xs font-medium rounded-full bg-primary-900/30 text-primary-400">
                                            {user.subscription_tier}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                                        {user.total_events}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                                        {user.days_since_last_active !== null
                                            ? `${Math.round(user.days_since_last_active)} days ago`
                                            : 'Never'
                                        }
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                                        <div className="flex items-center">
                                            <div className="flex-1 bg-slate-700 rounded-full h-2 mr-2">
                                                <div
                                                    className={`h-2 rounded-full ${user.latest_churn_prediction && user.latest_churn_prediction >= 0.7
                                                            ? 'bg-red-500'
                                                            : user.latest_churn_prediction && user.latest_churn_prediction >= 0.4
                                                                ? 'bg-yellow-500'
                                                                : 'bg-green-500'
                                                        }`}
                                                    style={{ width: `${(user.latest_churn_prediction || 0) * 100}%` }}
                                                />
                                            </div>
                                            <span className={`text-xs font-medium ${risk.color}`}>
                                                {user.latest_churn_prediction !== null
                                                    ? `${(user.latest_churn_prediction * 100).toFixed(1)}%`
                                                    : 'N/A'
                                                }
                                            </span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                                        {user.churned ? (
                                            <span className="px-2 py-1 text-xs font-medium rounded-full bg-red-900/30 text-red-400">
                                                Churned
                                            </span>
                                        ) : (
                                            <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-900/30 text-green-400">
                                                Active
                                            </span>
                                        )}
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default UserTable;
