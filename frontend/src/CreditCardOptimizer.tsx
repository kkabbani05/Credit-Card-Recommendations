import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './CreditCardOptimizer.css';

interface Transaction {
    category: string;
    total: number;
}

interface CreditCardRewards {
    [category: string]: number;

    Default: number;
}

interface CreditCard {
    name: string;
    annualFee: number;
    rewards: CreditCardRewards;
}

interface CardRewards {
    name: string;
    annualRewards: number;
    netRewards: number;
}

interface OptimalCombo {
    card: string;
    bestFor: string[];
}

interface TooltipProps {
    active?: boolean;
    payload?: any[];
    label?: string;
}

const CreditCardOptimizer: React.FC = () => {
    // Sample transaction data - in real app would come from API
    const transactions: Transaction[] = [
        { category: 'Groceries', total: 5600 },
        { category: 'Dining', total: 3200 },
        { category: 'Travel', total: 2800 },
        { category: 'Gas', total: 2400 },
        { category: 'Entertainment', total: 1800 },
        { category: 'Other', total: 4200 },
    ];

    // Credit card definitions
    const creditCards: CreditCard[] = [
        {
            name: 'Blue Cash Preferred',
            annualFee: 95,
            rewards: {
                'Groceries': 0.06,
                'Gas': 0.03,
                'Default': 0.01
            }
        },
        {
            name: 'Chase Sapphire Preferred',
            annualFee: 95,
            rewards: {
                'Dining': 0.03,
                'Travel': 0.03,
                'Default': 0.01
            }
        },
        {
            name: 'Capital One Savor',
            annualFee: 95,
            rewards: {
                'Dining': 0.04,
                'Entertainment': 0.04,
                'Groceries': 0.02,
                'Default': 0.01
            }
        }
    ];

    // Calculate rewards for each card
    const cardRewards: CardRewards[] = creditCards.map(card => {
        let totalRewards = 0;
        transactions.forEach(trans => {
            const rewardRate = card.rewards[trans.category] || card.rewards.Default;
            totalRewards += trans.total * rewardRate;
        });
        return {
            name: card.name,
            annualRewards: totalRewards,
            netRewards: totalRewards - card.annualFee
        };
    });

    // Calculate optimal card combination
    const getOptimalCombination = (): OptimalCombo[] => {
        let bestCombo: OptimalCombo[] = [];

        transactions.forEach(trans => {
            const bestCard = creditCards.reduce((best, card) => {
                const rate = card.rewards[trans.category] || card.rewards.Default;
                const bestRate = best.rewards[trans.category] || best.rewards.Default;
                return rate > bestRate ? card : best;
            }, creditCards[0]);

            const existingCombo = bestCombo.find(c => c.card === bestCard.name);
            if (!existingCombo) {
                bestCombo.push({
                    card: bestCard.name,
                    bestFor: [trans.category]
                });
            } else {
                existingCombo.bestFor.push(trans.category);
            }
        });

        return bestCombo;
    };

    const optimalCombo = getOptimalCombination();

    const formatCurrency = (value: number): string => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(value);
    };

    const CustomTooltip: React.FC<TooltipProps> = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="tooltip">
                    <p className="tooltip-label">{label}</p>
                    {payload.map((pld, index) => (
                        <p key={index} className="tooltip-value" style={{ color: pld.color }}>
                            {pld.name}: {formatCurrency(pld.value)}
                        </p>
                    ))}
                </div>
            );
        }
        return null;
    };

    return (
        <div className="optimizer-container">
            <div className="section-container">
                {/* Annual Spending Section */}
                <div className="card">
                    <h2 className="card-title">Annual Spending by Category</h2>
                        <div className="chart-container">
                        <BarChart
                            width={600}
                            height={240}
                            data={transactions}
                            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="category" />
                            <YAxis tickFormatter={formatCurrency} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="total" fill="#4F46E5" />
                        </BarChart>
                    </div>
                </div>

                {/* Potential Rewards Section */}
                <div className="card">
                    <h2 className="card-title">Potential Annual Rewards by Card</h2>
                    <div className="chart-container">
                        <BarChart
                            width={600}
                            height={240}
                            data={cardRewards}
                            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis tickFormatter={formatCurrency} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar
                                dataKey="netRewards"
                                fill="#10B981"
                                name="Net Rewards (after annual fee)"
                            />
                        </BarChart>
                    </div>
                </div>

                {/* Recommendations Section */}
                <div className="card">
                    <h2 className="card-title">Recommended Card Strategy</h2>
                    <div className="recommendations">
                        {optimalCombo.map((combo, index) => (
                            <div key={index} className="recommendation-card">
                                <h3 className="recommendation-title">{combo.card}</h3>
                                <p className="recommendation-text">
                                    Best for: {combo.bestFor.join(', ')}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CreditCardOptimizer;