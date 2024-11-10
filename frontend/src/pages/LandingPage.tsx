// LandingPage.tsx
import React, { useState, useRef, ChangeEvent, FormEvent } from 'react';
import { ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  Button,
  Box
} from '@mui/material';

interface FormData {
  username: string;
  password: string;
  income: string;
  age: string;
  oldestAccountLengthYears: string;
  credtScore: string;
  annualFeeAcceptance: string;
}

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);
  const [csvUploaded, setCsvUploaded] = useState<boolean>(false);
  const [file, setFile] = useState<File>();
  const [userInfoSubmitted, setUserInfoSubmitted] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [userJSON, setUserJSON] = useState<FormData | null>(null);  

  const [formData, setFormData] = useState<FormData>({
    username: '',
    password: '',
    income: '',
    age: '',
    oldestAccountLengthYears: '',
    credtScore: '',
    annualFeeAcceptance: ''
  });

  const handleFileUpload = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setFile(file);
    // console.log("FILE Sub: ", file);
    if (file) {
      if (file.type === 'text/csv') {
        setCsvUploaded(true);
      } else {
        alert('Please upload a CSV file only');
        event.target.value = '';
      }
    }
  };

  const handleFormChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFormSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const isFormValid = Object.values(formData).every(value => value !== '');
    
    if (isFormValid) {
      setUserJSON(formData);
      // console.log("FormData Sub: ", formData);
      setUserInfoSubmitted(true);
      setIsDialogOpen(false);
    } else {
      alert('Please fill all fields');
    }
  };

  const handleGetMatched = () => {
    if (csvUploaded && userInfoSubmitted) {
      navigate('/credit-dashboard');
    } else {
      alert('Please complete both the transaction history upload and user info form first');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      <nav className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <div className="text-white text-xl font-semibold flex items-center">
            <div className="w-6 h-6 bg-lime-400 rounded-full mr-2" />
            CardAdvise
          </div>
        </div>  
      </nav>

      <main className="max-w-6xl mx-auto px-6 pt-20">
        <div className="text-center mb-16">
          <div className="inline-block mb-4 px-4 py-2 bg-slate-800/50 rounded-full text-gray-300 text-sm">
            AI Powered Recommendations
          </div>
          <h1 className="text-6xl font-bold text-white mb-6">
            Find Your Perfect <span className="text-lime-400">Card Match</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Experience personalized credit card recommendations based on your spending habits and lifestyle.
            Get matched with the best rewards programs instantly.
          </p>
          <div className="flex justify-center space-x-4 mb-5">
            <input
              type="file"
              accept=".csv"
              ref={fileInputRef}
              onChange={handleFileUpload}
              className="hidden"
            />
            <Button 
              variant="outlined"
              sx={{
                color: 'white',
                borderColor: 'gray',
                '&:hover': {
                  backgroundColor: csvUploaded ? '#84cc16' : 'rgba(30, 41, 59, 0.5)',
                  borderColor: 'gray'
                },
                backgroundColor: csvUploaded ? '#84cc16' : 'transparent'
              }}
              onClick={() => fileInputRef.current?.click()}
            >
              {csvUploaded ? 'CSV Uploaded ✓' : 'Upload Transaction History'}
            </Button>
            <Button 
              variant="outlined"
              sx={{
                color: 'white',
                borderColor: 'gray',
                '&:hover': {
                  backgroundColor: userInfoSubmitted ? '#84cc16' : 'rgba(30, 41, 59, 0.5)',
                  borderColor: 'gray'
                },
                backgroundColor: userInfoSubmitted ? '#84cc16' : 'transparent'
              }}
              onClick={() => setIsDialogOpen(true)}
            >
              {userInfoSubmitted ? 'Info Submitted ✓' : 'Enter User Info'}
            </Button>
          </div>
          <div className="flex justify-center space-x-4">
            <Button 
              variant="contained"
              sx={{
                backgroundColor: csvUploaded && userInfoSubmitted ? '#84cc16' : '#334155',
                color: csvUploaded && userInfoSubmitted ? '#0f172a' : '#94a3b8',
                '&:hover': {
                  backgroundColor: csvUploaded && userInfoSubmitted ? '#65a30d' : '#334155'
                },
                '&.Mui-disabled': {
                  backgroundColor: '#334155',
                  color: '#94a3b8'
                }
              }}
              onClick={handleGetMatched}
              disabled={!csvUploaded || !userInfoSubmitted}
              endIcon={<ChevronRight />}
            >
              Get Matched Now
            </Button>
          </div>
        </div>

        {/* User Info Dialog */}
        <Dialog 
          open={isDialogOpen} 
          onClose={() => setIsDialogOpen(false)}
          PaperProps={{
            sx: {
              backgroundColor: '#1e293b',
              color: 'white'
            }
          }}
        >
          <DialogTitle>Enter User Information</DialogTitle>
          <DialogContent>
            <Box component="form" onSubmit={handleFormSubmit} sx={{ mt: 2 }}>
              {Object.keys(formData).map((field) => (
                <TextField
                  key={field}
                  fullWidth
                  margin="normal"
                  label={field.replace(/([A-Z])/g, ' $1').trim()}
                  name={field}
                  type={field === 'password' ? 'password' : 'text'}
                  value={formData[field as keyof FormData]}
                  onChange={handleFormChange}
                  sx={{
                    '& .MuiInputLabel-root': { color: 'gray' },
                    '& .MuiOutlinedInput-root': {
                      color: 'white',
                      '& fieldset': { borderColor: 'gray' },
                      '&:hover fieldset': { borderColor: 'white' },
                      '&.Mui-focused fieldset': { borderColor: '#84cc16' }
                    }
                  }}
                />
              ))}
              <Button 
                type="submit"
                fullWidth
                variant="contained"
                sx={{ 
                  mt: 3, 
                  mb: 2,
                  backgroundColor: '#84cc16',
                  '&:hover': {
                    backgroundColor: '#65a30d'
                  }
                }}
              >
                Submit
              </Button>
            </Box>
          </DialogContent>
        </Dialog>

        {/* Card Preview Section */}
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900 to-transparent" />
          <div className="grid grid-cols-3 gap-6">
            {/* Preview sections remain unchanged */}
            <div className="bg-slate-800/50 p-6 rounded-2xl backdrop-blur">
              <div className="mb-4">
                <h3 className="text-white font-medium mb-2">Recommended Cards</h3>
                <div className="space-y-3">
                  <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden" />
                  <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden" />
                  <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden" />
                  <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden" />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-slate-800 to-slate-700 p-6 rounded-2xl">
              <div className="aspect-video bg-gradient-to-br from-slate-600 to-slate-700 rounded-xl p-4 text-white">
                <div className="flex justify-between items-start">
                  <div className="space-y-4">
                    <div className="w-12 h-8 bg-lime-400 rounded" />
                    <div className="text-lg">•••• 4242</div>
                  </div>
                  <div className="text-sm opacity-75">
                    {/* Removed CapitalOne logo reference */}
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-slate-800/50 p-6 rounded-2xl backdrop-blur">
              <div className="mb-4">
                <h3 className="text-white font-medium mb-2">Monthly Rewards</h3>
                <div className="text-3xl text-lime-400 font-semibold">
                  $234.50
                </div>
                <div className="text-gray-400 text-sm">
                  Potential Cashback
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default LandingPage;