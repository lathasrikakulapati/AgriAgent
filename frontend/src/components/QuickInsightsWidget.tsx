"use client";

import { AlertCircle, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { useLanguage } from "@/context/LanguageContext";

interface QuickStat {
  label: string;
  value: string;
  trend: "up" | "down" | "stable";
  trendValue: string;
  color: string;
}

export default function QuickInsightsWidget() {
  const { language } = useLanguage();
  const [stats, setStats] = useState<QuickStat[]>([]);
  const [alerts, setAlerts] = useState<string[]>([]);

  useEffect(() => {
    const month = new Date().getMonth() + 1;
    
    const quickStats: QuickStat[] = [];
    const warnings: string[] = [];

    const labels = {
      en: {
        rainExpected: "Rain expected", peanutPrice: "Peanut price", avgTemp: "Avg. Temperature",
        irrigNeeded: "Irrigation needed", high: "High", stable: "Stable", milletPrice: "Millet price",
        wheatPrice: "Wheat price", grainsPrice: "Grains price",
        optPlanting: "Optimal period to plant millet and peanuts",
        rainForecast: "Forecast: Moderate rain in 3-4 days",
        drySeason: "Dry season: Water your crops regularly",
        goodPeriod: "Good period for tomato and onion (Oct-Apr)",
      },
      fr: {
        rainExpected: "Pluies attendues", peanutPrice: "Prix arachide", avgTemp: "Température moy.",
        irrigNeeded: "Irrigation nécessaire", high: "Élevée", stable: "Stable", milletPrice: "Prix mil",
        wheatPrice: "Prix du blé", grainsPrice: "Prix des céréales",
        optPlanting: "Période optimale pour planter mil et arachide",
        rainForecast: "Prévisions : Pluies modérées dans 3-4 jours",
        drySeason: "Saison sèche : Arrosez régulièrement vos cultures maraîchères",
        goodPeriod: "Bonne période pour tomate et oignon (Oct-Avr)",
      },
      wo: {
        rainExpected: "Taw bi ñu suurlu", peanutPrice: "Njëg gerte", avgTemp: "Tangaay mooy.",
        irrigNeeded: "Nosal soxla na", high: "Kawe", stable: "Dagan", milletPrice: "Njëg dugub",
        wheatPrice: "Njëg blé", grainsPrice: "Njëg céréales",
        optPlanting: "Jamono bu baax ngir fàgg dugub ak gerte",
        rainForecast: "Wàllu: Taw ci 3-4 fan",
        drySeason: "Noor: Nosal sa tool ci bépp bés",
        goodPeriod: "Jamono bu baax ngir tamaate ak soble (Okt-Avr)",
      },
    };

    const l = labels[language] || labels.fr;

    if (month >= 6 && month <= 10) {
      quickStats.push({
        label: l.rainExpected,
        value: "75%",
        trend: "up",
        trendValue: "+12%",
        color: "#3b82f6",
      });
      quickStats.push({
        label: l.peanutPrice,
        value: "₹6,300 (MH)",
        trend: "up",
        trendValue: "+5%",
        color: "#22c55e",
      });
      warnings.push(l.optPlanting);
      warnings.push(l.rainForecast);
    } else {
      quickStats.push({
        label: l.avgTemp,
        value: "32\u00b0C",
        trend: "up",
        trendValue: "+2\u00b0",
        color: "#f59e0b",
      });
      quickStats.push({
        label: l.irrigNeeded,
        value: l.high,
        trend: "stable",
        trendValue: l.stable,
        color: "#3b82f6",
      });
      warnings.push(l.drySeason);
      warnings.push(l.goodPeriod);
    }

    quickStats.push({
      label: l.wheatPrice,
      value: "₹2,350 (PB)",
      trend: "stable",
      trendValue: "0%",
      color: "#8b5cf6",
    });
    quickStats.push({
      label: l.grainsPrice,
      value: "32,500 FCFA (DK)",
      trend: "up",
      trendValue: "+2%",
      color: "#f97316",
    });

    setStats(quickStats);
    setAlerts(warnings);
  }, [language]);

  const getTrendIcon = (trend: "up" | "down" | "stable") => {
    switch (trend) {
      case "up":
        return <TrendingUp size={14} />;
      case "down":
        return <TrendingDown size={14} />;
      default:
        return <Minus size={14} />;
    }
  };

  const getTrendColor = (trend: "up" | "down" | "stable") => {
    switch (trend) {
      case "up":
        return "#22c55e";
      case "down":
        return "#ef4444";
      default:
        return "#6b7280";
    }
  };

  return (
    <div className="space-y-4">
      {/* Alerts */}
      {alerts.map((alert, idx) => (
        <motion.div
          key={idx}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.1 }}
          style={{
            backgroundColor: "#fef3c7",
            border: "1px solid #fbbf24",
            borderRadius: "12px",
            padding: "0.875rem",
            display: "flex",
            gap: "0.75rem",
            alignItems: "start",
          }}
        >
          <AlertCircle size={18} style={{ color: "#f59e0b", flexShrink: 0, marginTop: "2px" }} />
          <p style={{ fontSize: "0.875rem", color: "#92400e", lineHeight: "1.4" }}>
            {alert}
          </p>
        </motion.div>
      ))}

      {/* Quick Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {stats.map((stat, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: (alerts.length * 0.1) + (idx * 0.1) }}
            whileHover={{ scale: 1.03 }}
            style={{
              backgroundColor: "var(--bg-card)",
              border: "1px solid var(--border)",
              borderRadius: "12px",
              padding: "1rem",
              cursor: "pointer",
              transition: "box-shadow 0.2s",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.08)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = "none";
            }}
          >
            <div
              className="text-xs font-medium mb-2"
              style={{ color: "var(--text-muted)" }}
            >
              {stat.label}
            </div>
            <div
              className="text-2xl font-bold mb-1"
              style={{ color: stat.color }}
            >
              {stat.value}
            </div>
            <div
              className="flex items-center gap-1 text-xs font-medium"
              style={{ color: getTrendColor(stat.trend) }}
            >
              {getTrendIcon(stat.trend)}
              <span>{stat.trendValue}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
