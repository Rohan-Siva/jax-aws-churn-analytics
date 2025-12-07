import React from 'react';

interface MetricsCardProps {
    title: string;
    value: string | number;
    subtitle?: string;
    icon?: React.ReactNode;
    trend?: {
        value: number;
        isPositive: boolean;
    };
}

const MetricsCard: React.FC<MetricsCardProps> = ({ title, value, subtitle, icon, trend }) => {
    return (
        <div className="metric-card">
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <p className="text-sm font-medium text-slate-400">{title}</p>
                    <p className="mt-2 text-3xl font-bold text-white">{value}</p>
                    {subtitle && (
                        <p className="mt-1 text-sm text-slate-500">{subtitle}</p>
                    )}
                </div>
                {icon && (
                    <div className="flex-shrink-0 ml-4">
                        <div className="w-12 h-12 bg-primary-900/30 rounded-lg flex items-center justify-center text-primary-400">
                            {icon}
                        </div>
                    </div>
                )}
            </div>
            {trend && (
                <div className="mt-4 flex items-center">
                    <span className={`text-sm font-medium ${trend.isPositive ? 'text-green-400' : 'text-red-400'}`}>
                        {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
                    </span>
                    <span className="text-sm text-slate-500 ml-2">vs last period</span>
                </div>
            )}
        </div>
    );
};

export default MetricsCard;
