import React, { useEffect, useState, useRef } from "react";
import { ArrowUp, ArrowDown } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Legend,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import CreditCardInfo from "../components/CreditCardInfo";
import { Link, Navigate, useLocation } from "react-router-dom";

const API_BASE_URL = "http://127.0.0.1:8000";

interface ScoreRange {
  min: number;
  max: number;
  color: string;
  rating: string;
}

interface PointsPerDollar {
  [key: string]: number | undefined;

  travel: number;
  dining: number;
  onlineGrocery: number;
  streaming: number;
  other: number;
  hotel: number;
  rentalCar: number;
  vacationRental: number;
}

interface SignUpBonus {
  points?: number | undefined;
  miles?: number | undefined;
  minimumSpend: number;
  timeFrameMonths: number;
}

interface Rewards {
  pointsPerDollar: PointsPerDollar;
  signUpBonus: SignUpBonus;
}

interface CardData {
  cardName: string;
  cardType: string;
  issuer: string;
  annualFee: number;
  APR: string;
  rewards: Rewards;
  benefits: string[];
  creditCardScoreMin: number;
  creditCardScoreMax: number;
  linkToApply: string;
  countryOfOrigin: string;
  difficulty_rating: number;
}

interface CreditCardRec {
  rec_reasoning: string;
  card_name: string;
  card_info: CardData;
}

interface RecommendationResponse {
  global_reasoning: string;
  recommendations: CreditCardRec[];
}

interface LocationState {
  recommendations: RecommendationResponse;
  userInfo: {
    username: string;
    income: number;
    age: number;
    oldestAccountLengthYears: number;
    creditScore: number;
    annualFeeWillingness: number;
  };
  transactionData: Array<{ [key: string]: string | number }>;
}

const scoreRanges: ScoreRange[] = [
  { min: 760, max: 850, color: "#00b300", rating: "Excellent" },
  { min: 620, max: 659, color: "#FFA07A", rating: "Below Average" },
  { min: 700, max: 759, color: "#90EE90", rating: "Very Good" },
  { min: 580, max: 619, color: "#FF8C00", rating: "Poor" },
  { min: 660, max: 699, color: "#FFFF00", rating: "Good" },
  { min: 300, max: 579, color: "#FF0000", rating: "Very Poor" }
];

interface MonthlySpending {
  travel: number;
  dining: number;
  onlineGrocery: number;
  streaming: number;
  other: number;
  hotel: number;
  rentalCar: number;
  vacationRental: number;
}

const averageMonthlySpending: MonthlySpending = {
  travel: 500,
  dining: 400,
  onlineGrocery: 600,
  streaming: 50,
  other: 1000,
  hotel: 200,
  rentalCar: 100,
  vacationRental: 200
};

const calculateMonthlySavings = (
  pointsPerDollar: PointsPerDollar,
  spending: MonthlySpending
): number => {
  let totalPoints = 0;

  // Calculate points earned in each category
  Object.keys(spending).forEach((category) => {
    const spend = spending[category as keyof MonthlySpending];
    const multiplier = pointsPerDollar[category as keyof PointsPerDollar] || 1;
    totalPoints += spend * multiplier;
  });

  // Convert points to dollars (assuming 1 point = 1 cent)
  return totalPoints * 0.01;
};

const getScoreColor = (score: number): string => {
  const range = scoreRanges.find(
    (range) => score >= range.min && score <= range.max
  );
  return range ? range.color : scoreRanges[scoreRanges.length - 1].color;
};

const getScoreRating = (score: number): string => {
  const range = scoreRanges.find(
    (range) => score >= range.min && score <= range.max
  );
  return range ? range.rating : "Very Poor";
};

const Dashboard: React.FC = () => {
  const location = useLocation();
  const state = location.state as LocationState;
  const { recommendations, userInfo, transactionData } = state;

  const [currentScore, setCurrentScore] = useState<number>(0);
  const [expandedCard, setExpandedCard] = useState<string | null>(null);
  const [expandAnimation, setExpandAnimation] = useState<boolean>(false);
  const cardRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});

  const [graphData, setGraphData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const targetScore = userInfo.creditScore;
  const maxScore = 850;

  const radius = 85;
  const circumference = 2 * Math.PI * radius;
  const fillOffset = circumference - (currentScore / maxScore) * circumference;

  useEffect(() => {
    fetchGraphData();
  }, []);

  const fetchGraphData = async () => {
    try {
      setLoading(true);

      const response = await fetch("http://localhost:8000/api/graph", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          transaction_info: transactionData,
          rec_info: recommendations.recommendations
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to fetch graph data");
      }

      const data = await response.json();
      console.log("data", data);

      processGraphData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      console.error("Error fetching graph data:", err);
    } finally {
      setLoading(false);
    }
  };

  const processGraphData = (data: any) => {
    const { points_per_card_per_year, total_points_per_year } = data;

    // Transform the data for the graph
    const transformedData = Object.entries(points_per_card_per_year).map(
      ([year, cardPoints]: [string, any]) => {
        const dataPoint: any = { year };

        // Add points for each card
        Object.entries(cardPoints).forEach(
          ([cardName, points]: [string, any]) => {
            dataPoint[cardName] = parseFloat((points * 0.01).toFixed(2)); // Convert points to dollars
          }
        );

        // Add total points for the year
        dataPoint.combinedSavings = parseFloat(
          (total_points_per_year[year] * 0.01).toFixed(2)
        );

        return dataPoint;
      }
    );

    setGraphData(transformedData);
  };

  // Replace the existing chart section with this updated version
  // Define your color palette
  const colorPalette = [
    "#8884d8", // Purple
    "#82ca9d", // Green
    "#ffc658", // Yellow
    "#ff7300", // Orange
    "#0088FE", // Blue
    "#00C49F", // Teal
    "#FFBB28", // Gold
    "#FF8042" // Coral
    // Add more colors if needed
  ];

  const renderChart = () => {
    if (loading)
      return <div className="text-center">Loading graph data...</div>;
    if (error)
      return <div className="text-center text-red-500">Error: {error}</div>;
    if (!graphData) return null;

    return (
      <div className="h-64">
        <ResponsiveContainer width="95%" height="130%">
          <LineChart
            data={graphData}
            margin={{ top: 25, right: 30, bottom: 50, left: 60 }} // Increase left and bottom margins
          >
            <XAxis
              dataKey="year"
              stroke="#94a3b8"
              label={{
                value: "Year",
                position: "insideBottom",
                dy: 20, // Pushes the label down further
                style: {
                  textAnchor: "middle",
                  fontSize: "18px", // Larger font size
                  fill: "#94a3b8"
                }
              }}
              tick={{ fontSize: "14px", fill: "#94a3b8" }} // Increase tick font size
            />
            <YAxis
              stroke="#94a3b8"
              tickFormatter={(value) => `${value}`}
              label={{
                value: "Total Points",
                angle: -90,
                position: "insideLeft",
                dy: -10,
                dx: -40,
                style: {
                  textAnchor: "middle",
                  fontSize: "18px", // Larger font size
                  fill: "#94a3b8"
                }
              }}
              tick={{ fontSize: "14px", fill: "#94a3b8" }} // Increase tick font size
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#1e293b",
                border: "none",
                borderRadius: "0.5rem"
              }}
              formatter={(value: number) => [`$${value.toFixed(2)}`, ""]}
            />
            <Legend
              verticalAlign="bottom"
              wrapperStyle={{ paddingTop: "20px", fontSize: "16px" }} // Pushes legend down and increases font size
            />

            {recommendations.recommendations.map((card, index) => (
              <Line
                key={card.card_info.cardName}
                type="monotone"
                dataKey={card.card_info.cardName}
                name={`${card.card_info.cardName} Rewards`}
                stroke={colorPalette[index % colorPalette.length]}
                strokeWidth={2}
                dot={{ fill: colorPalette[index % colorPalette.length] }}
              />
            ))}

            <Line
              type="monotone"
              dataKey="combinedSavings"
              name="Combined Rewards"
              stroke="#ffffff"
              strokeWidth={3}
              strokeDasharray="5 5"
              dot={{ fill: "#ffffff" }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  };

  useEffect(() => {
    const animationDuration = 2000;
    const steps = 60;
    const increment = targetScore / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= targetScore) {
        setCurrentScore(targetScore);
        clearInterval(timer);
      } else {
        setCurrentScore(Math.floor(current));
      }
    }, animationDuration / steps);

    return () => clearInterval(timer);
  }, []);

  // Redirect to landing page if accessed directly without data
  if (!state?.recommendations) {
    return <Navigate to="/" replace />;
  }

  const handleCardClick = (cardName: string) => {
    const cardElement = cardRefs.current[cardName];
    const currentPosition = window.scrollY;
    const cardPosition = cardElement?.getBoundingClientRect().top ?? 0;
    const offset = cardPosition + currentPosition;

    if (expandedCard === cardName) {
      setExpandAnimation(false);
      setTimeout(() => {
        setExpandedCard(null);
      }, 500); // Increased timeout for slower animation
    } else {
      // Save the current scroll position
      window.scrollTo({
        top: offset - 100, // Adjust this value to control how much of the card is visible
        behavior: "smooth"
      });

      setExpandedCard(cardName);
      setTimeout(() => {
        setExpandAnimation(true);
      }, 50);
    }
  };

  // Function to safely get max points
  const getMaxPoints = (pointsPerDollar: PointsPerDollar): number => {
    return Math.max(
      ...Object.values(pointsPerDollar).filter(
        (points): points is number => points !== undefined
      )
    );
  };

  // Generate 12 months of data for each card
  const generateSavingsData = () => {
    const months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec"
    ];

    return months.map((month, index) => {
      const monthData: any = { month };
      let totalSavings = 0;

      // Calculate cumulative savings for each card
      recommendations.recommendations.forEach((card) => {
        const monthlySaving = calculateMonthlySavings(
          card.card_info.rewards.pointsPerDollar,
          averageMonthlySpending
        );
        const cumulativeSaving = monthlySaving * (index + 1);
        monthData[card.card_info.cardName] = cumulativeSaving;
        totalSavings += cumulativeSaving;
      });

      // Add combined savings
      monthData.combinedSavings = totalSavings;

      return monthData;
    });
  };

  const savingsData = generateSavingsData();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white p-6">
      {/* Navigation */}
      <nav className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-8">
          <div className="text-xl font-semibold flex items-center">
              <div className="w-6 h-6 bg-lime-400 rounded-full mr-2" />
              <Link to="/">
              NoCapAd
            </Link>
          </div>
        </div>
      </nav>

      <div className="grid grid-cols-12 gap-6">
        {/* Credit Score Section */}
        <div className="col-span-5 bg-slate-800/50 rounded-2xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-3xl font-semibold">Credit Score</h2>
            <button className="text-sm text-gray-400 hover:text-white">
              Details
            </button>
          </div>

          <div className="relative flex justify-center items-center mb-8">
            <div className="relative w-48 h-48">
              <svg
                className="w-full h-full -rotate-90 transform"
                viewBox="0 0 200 200"
              >
                {/* Background circle */}
                <circle
                  cx="100"
                  cy="100"
                  r={radius}
                  stroke="currentColor"
                  strokeWidth="12"
                  fill="none"
                  className="text-slate-700"
                />

                {/* Animated progress circle */}
                <circle
                  cx="100"
                  cy="100"
                  r={radius}
                  strokeWidth="12"
                  fill="none"
                  strokeLinecap="round"
                  style={{
                    stroke: getScoreColor(currentScore),
                    strokeDasharray: circumference,
                    strokeDashoffset: fillOffset,
                    transition:
                      "stroke-dashoffset 0.1s ease-out, stroke 0.1s ease-out"
                  }}
                />
              </svg>

              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-5xl font-bold">{currentScore}</div>
                  <div className="text-sm text-gray-400 mt-2">
                    {getScoreRating(currentScore)}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Score Range Legend */}
          <div className="grid grid-cols-2 gap-2 text-sm mb-6">
            {scoreRanges.map((range, index) => (
              <div
                key={index}
                className="flex items-center space-x-2"
                style={{
                  opacity:
                    currentScore >= range.min && currentScore <= range.max
                      ? 1
                      : 0.5
                }}
              >
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: range.color }}
                />
                <span>{`${range.min}-${range.max}: ${range.rating}`}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Financial Plans Section */}
        <div className="col-span-7 bg-slate-800/50 rounded-2xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-3xl font-semibold">Projected Rewards Value</h2>
          </div>
          {renderChart()}
          <p className="text-sm font-semibold mt-12 text-gray-500">
            *The combined total assumes you use the credit card the leads to the
            most rewards for each category with no overlap, so one card per
            category
          </p>
        </div>

        {/* Credit Card Recommendation Section */}
        <div className="col-span-12 flex flex-col items-center">
          <h2 className="text-3xl font-semibold mb-6">
            Credit Card Recommendation
          </h2>
          <div className="flex flex-col gap-6 w-[50vw]">
            {recommendations.recommendations.map((card, index) => (
              <div
                key={index}
                ref={(el) => (cardRefs.current[card.card_info.cardName] = el)}
                className="bg-slate-800/50 rounded-2xl transition-all duration-500 ease-in-out overflow-hidden"
              >
                <div
                  className="p-6 cursor-pointer hover:bg-slate-800/70 transition-colors"
                  onClick={() => handleCardClick(card.card_info.cardName)}
                >
                  <div className="flex justify-between items-center mb-4">
                    <div className="text-gray-400 text-xl">
                      {card.card_info.cardName}
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex items-center gap-4 text-sm">
                        <span className="px-2 py-1 rounded-full bg-lime-400/20 text-lime-400">
                          ${card.card_info.annualFee}/year
                        </span>
                        <span className="px-2 py-1 rounded-full bg-yellow-400/20 text-yellow-400">
                          {card.card_info.creditCardScoreMin}+ Credit Score
                        </span>
                        <span className="px-2 py-1 rounded-full bg-blue-400/20 text-blue-400">
                          {getMaxPoints(card.card_info.rewards.pointsPerDollar)}
                          x Max Points
                        </span>
                      </div>
                      {expandedCard === card.card_info.cardName ? (
                        <ArrowUp className="w-4 h-4 text-gray-400" />
                      ) : (
                        <ArrowDown className="w-4 h-4 text-gray-400" />
                      )}
                    </div>
                  </div>
                </div>

                <div
                  className={`
                    transition-all
                    duration-500
                    ease-in-out
                    ${
                      expandedCard === card.card_info.cardName
                        ? "max-h-[2000px] opacity-100"
                        : "max-h-0 opacity-0"
                    }
                  `}
                >
                  <div className="px-6 pb-6">
                    <div className="border-t border-slate-700 pt-6">
                      <CreditCardInfo recReason={card.rec_reasoning} cardData={card.card_info} />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
