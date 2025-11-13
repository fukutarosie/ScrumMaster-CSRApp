'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import Header from '../../../components/Header';
import Alert from '../../../components/Alert';
import { useToast } from '../../../components/ToastProvider';
import Link from 'next/link';

export default function CompletedMatches() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const toast = useToast();
  
  // Date filters
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [dateError, setDateError] = useState('');
  const [serviceType, setServiceType] = useState('');
  const [serviceTypes, setServiceTypes] = useState([]);
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);

  const getToken = () => localStorage.getItem('token');

  useEffect(() => {
    // Check auth
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    if (!token || !userData) {
      router.push('/');
      return;
    }

    const parsedUser = JSON.parse(userData);
    if (parsedUser.role.role_name !== 'PIN') {
      router.push('/');
      return;
    }

    setUser(parsedUser);
    fetchCompletedMatches();
    fetchServiceTypes();
  }, [router]);

  useEffect(() => {
    if (user) {
      fetchCompletedMatches();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPage, startDate, endDate, serviceType]);

  const fetchCompletedMatches = async () => {
    setLoading(true);
    setError('');
    
    try {
      const token = getToken();
      if (!token) {
        setError('Not authenticated');
        toast.error('Please log in again');
        setLoading(false);
        return;
      }

      const params = {
        page: currentPage,
        limit: 10
      };
      
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;
      if (serviceType) params.service_type = serviceType;

      console.log('[DEBUG] Fetching completed matches with params:', params);

      const response = await axios.get('http://localhost:5000/api/requests/history', {
        headers: { 'Authorization': `Bearer ${token}` },
        params
      });

      console.log('[DEBUG] History response:', response.data);

      if (response.data.success) {
        setMatches(response.data.data || []);
        
        if (response.data.pagination) {
          setTotalPages(response.data.pagination.pages || 1);
          setTotalItems(response.data.pagination.total || 0);
        }
      } else {
        setError(response.data.message || 'Failed to fetch completed matches');
        toast.error(response.data.message || 'Failed to fetch completed matches');
      }
    } catch (err) {
      console.error('[ERROR] Failed to fetch completed matches:', err);
      console.error('[ERROR] Error details:', err.response?.data);
      
      const msg = err.response?.data?.message || err.message || 'Failed to fetch completed matches';
      setError(msg);
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  const fetchServiceTypes = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/requests/service-types');
      const actualData = Array.isArray(response.data) ? response.data[0] : response.data;
      if (actualData?.success) {
        setServiceTypes(actualData.data || []);
      }
    } catch (err) {
      console.error('Failed to load service types', err);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  if (loading && matches.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Header title="Completed Matches" subtitle="View your fulfilled requests and CSR matches" />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <Link href="/pin">
            <button className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-semibold">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Dashboard
            </button>
          </Link>
        </div>
        {error && <Alert type="error" message={error} onClose={() => setError('')} />}

        {/* Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            🔍 Filter Your History
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">From Date</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => {
                  const newStartDate = e.target.value;
                  setStartDate(newStartDate);
                  setCurrentPage(1);
                  
                  // Validate date range
                  if (endDate && newStartDate && new Date(newStartDate) > new Date(endDate)) {
                    setDateError('From Date cannot be after To Date');
                  } else {
                    setDateError('');
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${dateError ? 'border-red-500' : 'border-gray-300'}`}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">To Date</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => {
                  const newEndDate = e.target.value;
                  setEndDate(newEndDate);
                  setCurrentPage(1);
                  
                  // Validate date range
                  if (startDate && newEndDate && new Date(startDate) > new Date(newEndDate)) {
                    setDateError('To Date cannot be before From Date');
                  } else {
                    setDateError('');
                  }
                }}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${dateError ? 'border-red-500' : 'border-gray-300'}`}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Service Type</label>
              <select
                value={serviceType}
                onChange={(e) => {
                  setCurrentPage(1);
                  setServiceType(e.target.value);
                }}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Service Types</option>
                {serviceTypes.map((type) => (
                  <option key={type.id} value={type.service_name}>
                    {type.service_name}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={() => {
                  setStartDate('');
                  setEndDate('');
                  setDateError('');
                  setServiceType('');
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Clear Filters
              </button>
            </div>
          </div>
          
          {/* Date validation error */}
          {dateError && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-700">⚠️ {dateError}</p>
            </div>
          )}
        </div>

        {/* Summary Stats */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <p className="text-sm text-gray-600">
            Total completed matches: <span className="font-semibold">{totalItems}</span>
          </p>
        </div>

        {/* Completed Matches List */}
        <div className="space-y-6">
          {matches.length === 0 ? (
            <div className="bg-white rounded-lg shadow text-center py-12">
              <div className="text-6xl mb-4">🎉</div>
              <p className="text-gray-600 mb-2">No completed matches yet</p>
              <p className="text-sm text-gray-500">When your requests are fulfilled, they will appear here</p>
            </div>
          ) : (
            matches.map((match) => (
              <div key={match.id} className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-900 mb-2">{match.title}</h3>
                      <p className="text-sm text-gray-600 mb-2">{match.description}</p>
                      <div className="flex flex-wrap gap-2 mb-3">
                        <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                          {match.category}
                        </span>
                        {match.service_type && (
                          <span className="px-2 py-1 text-xs font-medium bg-purple-100 text-purple-800 rounded-full">
                            {match.service_type}
                          </span>
                        )}
                        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                          FULFILLED
                        </span>
                      </div>
                    </div>
                    <div className="text-right ml-4">
                      <p className="text-sm text-gray-500">Fulfilled on</p>
                      <p className="text-sm font-semibold text-gray-900">{formatDate(match.fulfilled_at)}</p>
                    </div>
                  </div>

                  {/* Location Info */}
                  {match.location_city && (
                    <div className="mb-4 pb-4 border-b border-gray-200">
                      <p className="text-sm text-gray-600">
                        📍 <span className="font-medium">{match.location_city}</span>
                        {match.location_detail && ` - ${match.location_detail}`}
                      </p>
                    </div>
                  )}

                  {/* CSR Match Details */}
                  {match.matched_csr && match.matched_csr.length > 0 ? (
                    <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded">
                      <h4 className="font-semibold text-green-900 mb-3">✅ Matched CSR Representative</h4>
                      {match.matched_csr.map((csr) => (
                        <div key={csr.id} className="space-y-3">
                          
                          {/* CSR Info Card */}
                          {csr.csr_user && (
                            <div className="bg-white p-3 rounded-lg border border-green-200">
                              <div className="flex items-center gap-3">
                                <div className="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                                  {csr.csr_user.full_name ? csr.csr_user.full_name.charAt(0).toUpperCase() : 'C'}
                                </div>
                                <div className="flex-1 min-w-0">
                                  <p className="text-lg font-bold text-gray-900 truncate">
                                    {csr.csr_user.full_name || `CSR User #${csr.csr_user_id}`}
                                  </p>
                                  <p className="text-sm text-gray-600">
                                    CSR Representative • ID: #{csr.csr_user.id}
                                  </p>
                                  {csr.csr_user.email && (
                                    <p className="text-xs text-gray-500 mt-1 truncate">
                                      📧 {csr.csr_user.email}
                                    </p>
                                  )}
                                </div>
                              </div>
                            </div>
                          )}
                          
                          <div className="grid grid-cols-2 gap-4 text-sm">
                            {csr.volunteered_hours && (
                              <div>
                                <p className="text-green-700 font-medium">Volunteer Rating</p>
                                <p className="text-green-900 text-xl font-bold">⭐ {csr.volunteered_hours}/5</p>
                              </div>
                            )}
                            {csr.completion_date && (
                              <div>
                                <p className="text-green-700 font-medium">Completion Date</p>
                                <p className="text-green-900">{formatDate(csr.completion_date)}</p>
                              </div>
                            )}
                          </div>


                          {csr.notes && (
                            <div className="text-sm bg-white p-3 rounded border border-green-100">
                              <p className="text-green-700 font-medium mb-1">📝 CSR Notes</p>
                              <p className="text-green-900 italic">"{csr.notes}"</p>
                            </div>
                          )}

                          {csr.feedback_from_pin && (
                            <div className="text-sm bg-yellow-50 p-3 rounded border border-yellow-200">
                              <p className="text-yellow-800 font-medium mb-1">💬 Your Feedback</p>
                              <p className="text-yellow-900 italic">"{csr.feedback_from_pin}"</p>
                            </div>
                          )}

                          {!csr.feedback_from_pin && (
                            <button
                              onClick={() => router.push(`/pin/request/${match.id}?action=feedback`)}
                              className="w-full text-sm text-blue-600 hover:text-blue-800 font-medium py-2 px-4 border border-blue-300 rounded-lg hover:bg-blue-50 transition"
                            >
                              + Add Feedback for {csr.csr_user?.full_name || 'this CSR'}
                            </button>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="bg-gray-50 border-l-4 border-gray-400 p-4 rounded">
                      <p className="text-gray-600 text-sm">
                        This request was marked as fulfilled but no CSR match details are available.
                      </p>
                    </div>
                  )}

                  {/* Request Details */}
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-gray-500">Created</p>
                        <p className="font-medium">{formatDate(match.created_at)}</p>
                      </div>
                      <div>
                        <p className="text-gray-500">CSR Views</p>
                        <p className="font-medium">👁️ {match.view_count || 0}</p>
                        <p className="text-xs text-gray-500 mt-1">Total times CSR reps viewed this request</p>
                      </div>
                      <div>
                        <p className="text-gray-500">CSR Shortlists</p>
                        <p className="font-medium">⭐ {match.shortlist_count || 0}</p>
                        <p className="text-xs text-gray-500 mt-1">Number of CSR reps who shortlisted this request</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="mt-6 flex justify-center">
            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
              <button
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                className="relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
                className="relative inline-flex items-center px-4 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </nav>
          </div>
        )}
      </main>
    </div>
  );
}
