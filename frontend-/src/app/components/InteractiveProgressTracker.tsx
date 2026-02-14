import { motion } from "motion/react";
import { CheckCircle2 } from "lucide-react";

interface Step {
  title: string;
  description: string;
  completed: boolean;
}

const steps: Step[] = [
  {
    title: "Upload Your Resume",
    description: "Share your professional background",
    completed: false
  },
  {
    title: "Define Your Dream Role",
    description: "Tell us where you want to go",
    completed: false
  },
  {
    title: "Set Your Commitment",
    description: "How much time can you dedicate?",
    completed: false
  },
  {
    title: "Get Your Roadmap",
    description: "Receive your personalized 30-day plan",
    completed: false
  }
];

interface InteractiveProgressTrackerProps {
  currentStep?: number;
}

export function InteractiveProgressTracker({ currentStep = 0 }: InteractiveProgressTrackerProps) {
  return (
    <motion.div
      className="w-full mb-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-2">Your Journey</h3>
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-400">
            Step {currentStep + 1} of {steps.length}
          </p>
          <p className="text-sm font-semibold text-indigo-400">
            {Math.round((currentStep / steps.length) * 100)}% Complete
          </p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden mb-8">
        <motion.div
          className="h-full bg-gradient-to-r from-indigo-600 to-blue-600"
          initial={{ width: "0%" }}
          animate={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
          transition={{ duration: 0.8, ease: "easeInOut" }}
        />
      </div>

      {/* Steps Timeline */}
      <div className="space-y-4">
        {steps.map((step, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: idx * 0.1 }}
            className="flex items-start gap-4 group cursor-pointer"
          >
            {/* Step Circle */}
            <div className="flex-shrink-0 relative">
              <motion.div
                className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                  idx < currentStep
                    ? "bg-gradient-to-br from-green-500 to-emerald-500"
                    : idx === currentStep
                    ? "bg-gradient-to-br from-indigo-600 to-blue-600"
                    : "bg-white/10"
                }`}
                whileHover={{ scale: 1.1 }}
              >
                {idx < currentStep ? (
                  <CheckCircle2 className="w-6 h-6 text-white" />
                ) : (
                  <span className={`text-sm font-semibold ${idx === currentStep ? "text-white" : "text-gray-400"}`}>
                    {idx + 1}
                  </span>
                )}
              </motion.div>

              {/* Loading Animation for Current Step */}
              {idx === currentStep && (
                <motion.div
                  className="absolute inset-0 rounded-full border-2 border-transparent border-t-indigo-400"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                />
              )}
            </div>

            {/* Step Content */}
            <div className="flex-1 pt-1">
              <h4 className={`font-semibold transition-colors ${
                idx <= currentStep ? "text-white" : "text-gray-500"
              }`}>
                {step.title}
              </h4>
              <p className="text-sm text-gray-400 mt-1">
                {step.description}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
