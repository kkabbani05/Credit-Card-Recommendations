import React from "react";
import {
  CreditCard,
  Award,
  DollarSign,
  Gift,
  Shield,
  Star,
  Sparkle
} from "lucide-react";

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

interface CreditCardRecommendationProps {
  recReason: string;
  cardData: CardData;
  className?: string;
}

const CreditCardRecommendation: React.FC<CreditCardRecommendationProps> = ({
  recReason,
  cardData,
  className = ""
}) => {
  return (
    <div className={`rounded-2xl p-8 w-full ${className}`}>
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-3">
            <CreditCard className="w-8 h-8 text-lime-400" />
            <h3 className="text-2xl font-bold">
              {cardData.cardName}
            </h3>
          </div>
          <p className="text-gray-400 mt-1">
            {cardData.issuer} • {cardData.cardType}
          </p>
        </div>
        <div className="flex flex-col items-end">
          <div className="text-lg font-semibold">
            ${cardData.annualFee}/year
          </div>
          <div className="text-sm text-gray-400">
            {cardData.APR} APR
          </div>
        </div>
      </div>

      {/* Rewards Section */}
      <div>
      <h4 className="flex items-center gap-2 text-lg font-semibold mb-4">
          <Sparkle className="w-5 h-5 text-lime-400" />
          Why the Recommendation?
      </h4>
      <div className="mb-7 text-left ml-4">
        {recReason}
      </div>
      </div>
      <div className="mb-8">
        <h4 className="flex items-center gap-2 text-lg font-semibold mb-4">
          <Award className="w-5 h-5 text-lime-400" />
          Rewards Rate
        </h4>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(cardData.rewards.pointsPerDollar)
            .filter(([_, points]) => points && points > 0) // Only show non-zero rewards
            .map(([category, points]) =>
              <div
                key={category}
                className="flex items-center justify-between bg-slate-800/50 rounded-lg p-3"
              >
                <span className="capitalize">
                  {category.replace(/([A-Z])/g, " $1").trim()}
                </span>
                <span className="font-semibold text-lime-400">
                  {points}x points
                </span>
              </div>
            )}
        </div>
      </div>

      {/* Sign Up Bonus */}
      <div className="mb-8">
        <h4 className="flex items-center gap-2 text-lg font-semibold mb-4">
          <Gift className="w-5 h-5 text-lime-400" />
          Sign Up Bonus
        </h4>
        <div className="bg-lime-400/10 rounded-lg p-4">
          {cardData.rewards.signUpBonus.points
            ? <div className="text-2xl font-bold text-lime-400 mb-2">
                {cardData.rewards.signUpBonus.points.toLocaleString()} points
              </div>
            :  null}
          <p className="text-sm text-gray-300">
            Spend ${cardData.rewards.signUpBonus.minimumSpend.toLocaleString()}{" "}
            in the first {cardData.rewards.signUpBonus.timeFrameMonths} months
          </p>
        </div>
      </div>

      {/* Benefits */}
      <div className="mb-8">
        <h4 className="flex items-center gap-2 text-lg font-semibold mb-4">
          <Shield className="w-5 h-5 text-lime-400" />
          Card Benefits
        </h4>
        <div className="grid grid-cols-2 gap-4">
          {cardData.benefits.map((benefit, index) =>
            <div
              key={index}
              className="flex items-start gap-2 bg-slate-700/30 rounded-lg p-3"
            >
              <Star className="w-4 h-4 text-lime-400 mt-1 flex-shrink-0" />
              <span className="text-sm">
                {benefit}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Credit Score Range */}
      <div className="mb-8">
        <h4 className="flex items-center gap-2 text-lg font-semibold mb-4">
          <DollarSign className="w-5 h-5 text-lime-400" />
          Required Credit Score
        </h4>
        <div className="bg-slate-700/30 rounded-lg p-4">
          <div className="flex justify-between items-center">
            <span>
              {cardData.creditCardScoreMin}
            </span>
            <div className="h-2 flex-1 mx-4 bg-slate-600 rounded-full overflow-hidden">
              <div
                className="h-full bg-lime-400"
                style={{
                  width: `${(cardData.creditCardScoreMax -
                    cardData.creditCardScoreMin) /
                    (850 - 300) *
                    100}%`
                }}
              />
            </div>
            <span>
              {cardData.creditCardScoreMax}
            </span>
          </div>
        </div>
      </div>

      <button
        className="w-full bg-lime-400 hover:bg-lime-500 text-slate-900 font-semibold py-3 px-6 rounded-lg transition-colors"
        onClick={() => window.open(cardData.linkToApply, "_blank")}
      >
        Apply Now
      </button>
    </div>
  );
};

export default CreditCardRecommendation;
