import { motion } from "motion/react";
import { useState } from "react";
import { Upload, Github, FileText, Check, FileCheck, Sparkles } from "lucide-react";
import { Slider } from "../components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../components/ui/select";
import { Textarea } from "../components/ui/textarea";
import { ConstellationBackground } from "../components/ConstellationBackground";
import { MotivationalTips } from "../components/MotivationalTips";
import { InteractiveProgressTracker } from "../components/InteractiveProgressTracker";
import { MotivatedButton } from "../components/MotivatedButton";
import { AchievementBadges } from "../components/AchievementBadges";

export function CareerSetupPage() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [linkedinFile, setLinkedinFile] = useState<File | null>(null);
  const [githubUrl, setGithubUrl] = useState("");
  const [dreamRole, setDreamRole] = useState("");
  const [customRole, setCustomRole] = useState("");
  const [weeklyHours, setWeeklyHours] = useState([10]);
  const [isDragging, setIsDragging] = useState(false);
  const [isLinkedinDragging, setIsLinkedinDragging] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const calculateProgress = () => {
    let completed = 0;
    if (uploadedFile) completed++;
    if (dreamRole) completed++;
    if (weeklyHours[0]) completed++;
    return completed;
  };

  const handleFileUpload = (file: File) => {
    if (file && (file.type === "application/pdf" || file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document")) {
      setUploadedFile(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFileUpload(file);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setTimeout(() => {
      console.log({
        uploadedFile,
        linkedinFile,
        githubUrl,
        dreamRole: dreamRole === "Other" ? customRole : dreamRole,
        weeklyHours: weeklyHours[0],
      });
      setIsSubmitting(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-[#0F172A] dark flex items-center justify-center p-6 relative overflow-hidden">
      {/* Background Elements */}
      <ConstellationBackground />

      <motion.div
        className="w-full max-w-4xl relative z-10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-sm font-semibold text-indigo-400">Career Setup</span>
          </div>
          <h2 className="text-3xl md:text-4xl font-semibold text-white mb-2">Your Personalized Career Plan</h2>
          <p className="text-gray-400">Let's build your path to success, step by step</p>
        </div>

        {/* Motivational Tips */}
        <MotivationalTips />

        {/* Interactive Progress Tracker */}
        <InteractiveProgressTracker currentStep={calculateProgress()} />

        {/* Main Card */}
        <div
          className="rounded-3xl p-8 md:p-12"
          style={{
            background: "rgba(30, 41, 59, 0.6)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(255, 255, 255, 0.08)",
            boxShadow:
              "0 0 60px rgba(99, 102, 241, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.05)",
          }}
        >
          <form onSubmit={handleSubmit} className="space-y-10">
            {/* Section 1: Resume Upload */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center text-sm font-bold text-white">
                  1
                </div>
                <h3 className="text-xl font-semibold text-white">
                  Your Resume
                </h3>
                <motion.span
                  animate={{ opacity: [1, 0.5, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="ml-auto text-xs text-indigo-400"
                >
                  {uploadedFile && "✓ Complete"}
                </motion.span>
              </div>
              
              <div
                className={`relative border-2 border-dashed rounded-2xl p-8 transition-all ${
                  isDragging
                    ? "border-indigo-500 bg-indigo-500/10"
                    : uploadedFile
                    ? "border-green-500/50 bg-green-500/5"
                    : "border-white/20 bg-white/5"
                }`}
                onDragOver={(e) => {
                  e.preventDefault();
                  setIsDragging(true);
                }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  id="resume"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                  className="hidden"
                />
                
                {uploadedFile ? (
                  <div className="flex items-center justify-center space-x-3">
                    <div className="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center">
                      <Check className="w-6 h-6 text-green-500" />
                    </div>
                    <div className="text-left">
                      <p className="text-white font-medium">{uploadedFile.name}</p>
                      <p className="text-sm text-gray-400">
                        {(uploadedFile.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={() => setUploadedFile(null)}
                      className="ml-auto text-sm text-indigo-400 hover:text-indigo-300"
                    >
                      Change
                    </button>
                  </div>
                ) : (
                  <label
                    htmlFor="resume"
                    className="flex flex-col items-center cursor-pointer"
                  >
                    <Upload className="w-12 h-12 text-indigo-400 mb-4" />
                    <p className="text-white mb-1">
                      Upload your Resume (PDF or DOCX)
                    </p>
                    <p className="text-sm text-gray-400">
                      Drag and drop or click to browse
                    </p>
                  </label>
                )}
              </div>

              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-sm text-gray-400 mt-4 flex items-center gap-2"
              >
                <span className="text-lg">💡</span>
                Your resume is the foundation. It shows us your unique journey and potential!
              </motion.p>
            </div>

            {/* Section 2: Profile Links */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center text-sm font-bold text-white">
                  2
                </div>
                <h3 className="text-xl font-semibold text-white">
                  Profile Documents
                </h3>
              </div>
              
              <div className="space-y-4">
                {/* LinkedIn Profile Document */}
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    LinkedIn Profile (PDF or DOCX)
                  </label>
                  <div
                    className={`relative border-2 border-dashed rounded-2xl p-6 transition-all ${
                      isLinkedinDragging
                        ? "border-indigo-500 bg-indigo-500/10"
                        : linkedinFile
                        ? "border-green-500/50 bg-green-500/5"
                        : "border-white/20 bg-white/5"
                    }`}
                    onDragOver={(e) => {
                      e.preventDefault();
                      setIsLinkedinDragging(true);
                    }}
                    onDragLeave={() => setIsLinkedinDragging(false)}
                    onDrop={(e) => {
                      e.preventDefault();
                      setIsLinkedinDragging(false);
                      const file = e.dataTransfer.files[0];
                      if (file && (file.type === "application/pdf" || file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document")) {
                        setLinkedinFile(file);
                      }
                    }}
                  >
                    <input
                      type="file"
                      id="linkedin"
                      accept=".pdf,.docx"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) {
                          setLinkedinFile(file);
                        }
                      }}
                      className="hidden"
                    />
                    
                    {linkedinFile ? (
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 rounded-full bg-green-500/20 flex items-center justify-center">
                            <FileCheck className="w-5 h-5 text-green-500" />
                          </div>
                          <div className="text-left">
                            <p className="text-white text-sm font-medium">{linkedinFile.name}</p>
                            <p className="text-xs text-gray-400">
                              {(linkedinFile.size / 1024).toFixed(2)} KB
                            </p>
                          </div>
                        </div>
                        <button
                          type="button"
                          onClick={() => setLinkedinFile(null)}
                          className="text-xs text-indigo-400 hover:text-indigo-300"
                        >
                          Remove
                        </button>
                      </div>
                    ) : (
                      <label
                        htmlFor="linkedin"
                        className="flex items-center cursor-pointer"
                      >
                        <Upload className="w-8 h-8 text-indigo-400 mr-3" />
                        <div className="text-left">
                          <p className="text-white text-sm">
                            Upload LinkedIn Profile
                          </p>
                          <p className="text-xs text-gray-400">
                            PDF or DOCX format
                          </p>
                        </div>
                      </label>
                    )}
                  </div>
                </div>

                {/* GitHub */}
                <div className="relative">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2 z-10">
                    <Github className="w-5 h-5 text-gray-400" />
                  </div>
                  <input
                    type="url"
                    value={githubUrl}
                    onChange={(e) => setGithubUrl(e.target.value)}
                    className="w-full pl-12 pr-4 py-4 bg-white/5 border border-white/10 rounded-2xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                    placeholder="GitHub Profile URL"
                  />
                </div>
              </div>
            </div>

            {/* Section 3: Dream Role Selection */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-orange-600 to-red-600 flex items-center justify-center text-sm font-bold text-white">
                  3
                </div>
                <h3 className="text-xl font-semibold text-white">
                  Your Dream Role
                </h3>
                <motion.span
                  animate={{ opacity: [1, 0.5, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="ml-auto text-xs text-indigo-400"
                >
                  {dreamRole && "✓ Selected"}
                </motion.span>
              </div>
              
              <Select value={dreamRole} onValueChange={setDreamRole}>
                <SelectTrigger className="w-full h-14 bg-white/5 border-white/10 rounded-2xl text-white">
                  <SelectValue placeholder="Select Your Dream Role" />
                </SelectTrigger>
                <SelectContent className="bg-[#1E293B] border-white/10">
                  <SelectItem value="Machine Learning Engineer">
                    Machine Learning Engineer
                  </SelectItem>
                  <SelectItem value="Full Stack Developer">
                    Full Stack Developer
                  </SelectItem>
                  <SelectItem value="Product Manager">
                    Product Manager
                  </SelectItem>
                  <SelectItem value="Data Scientist">
                    Data Scientist
                  </SelectItem>
                  <SelectItem value="UI/UX Designer">
                    UI/UX Designer
                  </SelectItem>
                  <SelectItem value="Other">
                    Other
                  </SelectItem>
                </SelectContent>
              </Select>

              {/* Custom Role Textarea */}
              {dreamRole === "Other" && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                  className="mt-4"
                >
                  <Textarea
                    value={customRole}
                    onChange={(e) => setCustomRole(e.target.value)}
                    placeholder="Describe your dream role or the kind of work you want to do"
                    className="w-full min-h-32 bg-white/5 border-white/10 rounded-2xl text-white placeholder-gray-500 focus:ring-2 focus:ring-indigo-500 resize-none"
                  />
                </motion.div>
              )}

              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-sm text-gray-400 mt-4 flex items-center gap-2"
              >
                <span className="text-lg">🎯</span>
                Your dream role is the target. We'll create a strategic path to get you there!
              </motion.p>
            </div>

            {/* Section 4: Weekly Time Commitment */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-600 to-emerald-600 flex items-center justify-center text-sm font-bold text-white">
                  4
                </div>
                <h3 className="text-xl font-semibold text-white">
                  Weekly Time Commitment
                </h3>
              </div>
              
              <div className="flex items-center justify-between mb-6 p-6 rounded-2xl bg-white/5 border border-white/10">
                <div>
                  <p className="text-sm text-gray-400 mb-1">Commitment Level</p>
                  <p className="text-lg text-gray-300">You're dedicating time to grow 💪</p>
                </div>
                <div className="text-right">
                  <span className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-blue-400 bg-clip-text text-transparent">
                    {weeklyHours[0]}
                  </span>
                  <span className="text-gray-400 block text-sm">hours/week</span>
                </div>
              </div>
              
              <Slider
                value={weeklyHours}
                onValueChange={setWeeklyHours}
                min={1}
                max={40}
                step={1}
                className="w-full"
              />
              
              <div className="flex justify-between mt-2 text-sm text-gray-500">
                <span>1 hr</span>
                <span>40 hrs</span>
              </div>
            </div>

            {/* Submit Button */}
            <motion.div className="space-y-4">
              <MotivatedButton
                onClick={handleSubmit}
                size="lg"
                motivationalText="Your roadmap awaits! ✨"
              >
                {isSubmitting ? "Creating Your Roadmap..." : "Generate My 30-Day Roadmap"}
              </MotivatedButton>
              
              <p className="text-center text-sm text-gray-400">
                ✨ Once submitted, our AI will analyze your profile and create a personalized 30-day career growth plan
              </p>
            </motion.div>
          </form>
        </div>

        {/* Achievement Badges */}
        <motion.div
          className="mt-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.6 }}
        >
          <AchievementBadges />
        </motion.div>
      </motion.div>
    </div>
  );
}