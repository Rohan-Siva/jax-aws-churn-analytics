import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import MetricsCard from './MetricsCard';
import PredictionChart from './PredictionChart';
import UserTable from './UserTable';
import type { AnalyticsData, UserAnalytics, PredictionTimeline } from '../types';

const Dashboard: React.FC = () => {
    const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
    const [users, setUsers] = useState<UserAnalytics[]>([]);
    const [timeline, setTimeline] = useState<PredictionTimeline[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

    const fetchData = async () => {
        try {
            setError(null);

            
            const [analyticsData, usersData, timelineData] = await Promise.all([
                api.getAnalytics(),
                api.getUserAnalytics(50),
                api.getPredictionTimeline(30),
            ]);

            setAnalytics(analyticsData);
            setUsers(usersData);
            setTimeline(timelineData);
            setLastUpdate(new Date());
            setLoading(false);
        } catch (err) {
            console.error('Error fetching data:', err);
            setError('Failed to load dashboard data. Please check if the backend is running.');
            setLoading(false);
        }
    };

    useEffect(() => {
        
        fetchData();

        
        const interval = setInterval(fetchData, 30000);

        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
                    <p className="mt-4 text-slate-400">Loading dashboard...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="card bg-red-900/20 border-red-800">
                <div className="flex items-center">
                    <svg className="w-6 h-6 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                        <h3 className="text-lg font-semibold text-red-400">Error</h3>
                        <p className="text-red-300">{error}</p>
                    </div>
                </div>
                <button
                    onClick={fetchData}
                    className="mt-4 btn-primary"
                >
                    Retry
                </button>
            </div>
        );
    }

    if (!analytics) {
        return null;
    }

    return (
        <div className="space-y-6">
            {}
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white">Overview</h2>
                    <p className="text-sm text-slate-400 mt-1">
                        Last updated: {lastUpdate.toLocaleTimeString()}
                    </p>
                </div>
                <button
                    onClick={fetchData}
                    className="btn-secondary flex items-center space-x-2"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>Refresh</span>
                </button>
            </div>

            {}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricsCard
                    title="Total Users"
                    value={analytics.total_users.toLocaleString()}
                    subtitle={`${analytics.active_users} active`}
                    icon={
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                    }
                />

                <MetricsCard
                    title="Churn Rate"
                    value={`${analytics.churn_rate}%`}
                    subtitle={`${analytics.churned_users} churned users`}
                    icon={
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                        </svg>
                    }
                />

                <MetricsCard
                    title="Avg Churn Probability"
                    value={`${(analytics.avg_churn_probability * 100).toFixed(1)}%`}
                    subtitle="Across all predictions"
                    icon={
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                    }
                />

                <MetricsCard
                    title="Model Accuracy"
                    value={analytics.model_accuracy ? `${(analytics.model_accuracy * 100).toFixed(1)}%` : 'N/A'}
                    subtitle={`Version: ${analytics.model_version}`}
                    icon={
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    }
                />
            </div>

            {}
            {timeline.length > 0 && (
                <PredictionChart data={timeline} />
            )}

            {}
            {users.length > 0 && (
                <UserTable users={users} />
            )}

            {}
            <div className="card bg-primary-900/20 border-primary-800">
                <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                        <svg className="w-8 h-8 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold text-white">JAX-Powered Predictions</h3>
                        <p className="text-slate-300 mt-1">
                            Using JIT-compiled JAX model for ultra-fast inference.
                            Model version <span className="font-mono text-primary-400">{analytics.model_version}</span> deployed.
                        </p>
                        <p className="text-sm text-slate-400 mt-2">
                            Total predictions made: <span className="font-semibold text-white">{analytics.total_predictions.toLocaleString()}</span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
