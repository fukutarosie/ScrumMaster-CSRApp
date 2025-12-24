'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '../../components/Header';
import axios from 'axios';
import { useToast } from '../../components/ToastProvider';
import { API_BASE_URL, apiUrl } from '@/config/api';

export default function PlatformDashboard() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  
  const [categories, setCategories] = useState([]);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [categoryForm, setCategoryForm] = useState({ service_name: '' });
  const [categoriesLoading, setCategoriesLoading] = useState(false);
  const [categoryError, setCategoryError] = useState('');
  
  const [reportType, setReportType] = useState('daily');
  const [reportDate, setReportDate] = useState(new Date().toISOString().split('T')[0]);
  const [reportData, setReportData] = useState(null);
  const [reportsLoading, setReportsLoading] = useState(false);
  const [reportError, setReportError] = useState('');
  
  const [stats, setStats] = useState({
    totalCategories: 0,
    activeUsers: 0,
    totalRequests: 0
  });
  const toast = useToast();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    if (!token || !userData) {
      router.push('/');
      return;
    }

    const user = JSON.parse(userData);
    if (user.role.role_name !== 'Platform Management') {
      router.push('/');
      return;
    }

    setUser(user);
    setLoading(false);
    fetchStats();
  }, [router]);

  useEffect(() => {
    if (activeTab === 'categories') {
      fetchCategories();
    } else if (activeTab === 'reports') {
      fetchReport();
    }
  }, [activeTab]);

  const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    };
  };

  const fetchStats = async () => {
    try {
      const [categoriesRes, dailyReportRes] = await Promise.all([
        axios.get(apiUrl('/api/platform/categories'), getAuthHeaders()),
        axios.get(apiUrl('/api/platform/reports/daily'), getAuthHeaders())
      ]);

      setStats({
        totalCategories: categoriesRes.data.data?.categories?.length || categoriesRes.data.data?.total || 0,
        activeUsers: dailyReportRes.data.data?.total_active_users || 0,
        totalRequests: dailyReportRes.data.data?.total_requests || 0
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
      toast.error('Failed to load platform overview stats.');
    }
  };

  const fetchCategories = async () => {
    setCategoriesLoading(true);
    setCategoryError('');
    try {
      const response = await axios.get(apiUrl('/api/platform/categories'), getAuthHeaders());
      if (response.data.success) {
        const data = response.data.data;
        const categoriesArray = data?.categories || (Array.isArray(data) ? data : []);
        setCategories(categoriesArray);
      } else {
        const message = response.data.message || 'Failed to fetch categories';
        setCategories([]);
        setCategoryError(message);
        toast.error(message);
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to fetch categories';
      setCategories([]);
      setCategoryError(message);
      toast.error(message);
    } finally {
      setCategoriesLoading(false);
    }
  };

  const searchCategories = async () => {
    if (!searchKeyword.trim()) {
      fetchCategories();
      return;
    }

    setCategoriesLoading(true);
    setCategoryError('');
    try {
      const response = await axios.get(
        apiUrl(`/api/platform/categories/search?keyword=${encodeURIComponent(searchKeyword)}`),
        getAuthHeaders()
      );
      if (response.data.success) {
        const data = response.data.data;
        const categoriesArray = data?.categories || (Array.isArray(data) ? data : []);
        setCategories(categoriesArray);
        if (categoriesArray.length === 0) {
          toast.info('No categories matched that keyword.');
        } else {
          toast.success(`Showing ${categoriesArray.length} result${categoriesArray.length === 1 ? '' : 's'}.`);
        }
      } else {
        const message = response.data.message || 'Failed to search categories';
        setCategories([]);
        setCategoryError(message);
        toast.error(message);
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to search categories';
      setCategories([]);
      setCategoryError(message);
      toast.error(message);
    } finally {
      setCategoriesLoading(false);
    }
  };

  const handleCreateCategory = async (e) => {
    e.preventDefault();
    setCategoryError('');
    try {
      const response = await axios.post(
        apiUrl('/api/platform/categories'),
        categoryForm,
        getAuthHeaders()
      );
      if (response.data.success) {
        setIsCreateModalOpen(false);
        setCategoryForm({ service_name: '' });
        fetchCategories();
        fetchStats();
        toast.success('Service category created successfully.');
      } else {
        const message = response.data.message || 'Failed to create category';
        setCategoryError(message);
        toast.error(message);
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to create category';
      setCategoryError(message);
      toast.error(message);
    }
  };

  const handleUpdateCategory = async (e) => {
    e.preventDefault();
    setCategoryError('');
    try {
      const response = await axios.put(
        apiUrl(`/api/platform/categories/${selectedCategory.id}`),
        categoryForm,
        getAuthHeaders()
      );
      if (response.data.success) {
        setIsEditModalOpen(false);
        setSelectedCategory(null);
        setCategoryForm({ service_name: '' });
        fetchCategories();
        toast.success('Category updated successfully.');
      } else {
        const message = response.data.message || 'Failed to update category';
        setCategoryError(message);
        toast.error(message);
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to update category';
      setCategoryError(message);
      toast.error(message);
    }
  };

  const handleDeleteCategory = async () => {
    setCategoryError('');
    try {
      const response = await axios.delete(
        `${API_URL}/api/platform/categories/${selectedCategory.id}`,
        getAuthHeaders()
      );
      if (response.data.success) {
        setIsDeleteModalOpen(false);
        setSelectedCategory(null);
        fetchCategories();
        fetchStats();
        toast.success('Category removed successfully.');
      } else {
        const message = response.data.message || 'Failed to delete category';
        setCategoryError(message);
        toast.error(message);
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to delete category';
      setCategoryError(message);
      toast.error(message);
    }
  };

  const openEditModal = (category) => {
    setSelectedCategory(category);
    setCategoryForm({ service_name: category.service_name });
    setIsEditModalOpen(true);
  };

  const openDeleteModal = (category) => {
    setSelectedCategory(category);
    setIsDeleteModalOpen(true);
  };

  const fetchReport = async ({ showToastOnSuccess = false } = {}) => {
    setReportsLoading(true);
    setReportError('');
    try {
      let url = '';
      if (reportType === 'daily') {
        url = apiUrl(`/api/platform/reports/daily?date=${reportDate}`);
      } else if (reportType === 'weekly') {
        url = apiUrl(`/api/platform/reports/weekly?start_date=${reportDate}`);
      } else if (reportType === 'monthly') {
        const month = reportDate.substring(0, 7);
        url = apiUrl(`/api/platform/reports/monthly?month=${month}`);
      }
      
      const response = await axios.get(url, getAuthHeaders());
      if (response.data.success) {
        setReportData(response.data.data);
        if (showToastOnSuccess) {
          toast.success('Report generated successfully.');
        }
      } else {
        const message = response.data.message || 'Failed to fetch report';
        setReportError(message);
        if (showToastOnSuccess) {
          toast.error(message);
        }
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to fetch report';
      setReportError(message);
      toast.error(message);
    } finally {
      setReportsLoading(false);
    }
  };

  if (loading) {
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
      <Header title="Platform Management Dashboard" subtitle={`Welcome, ${user?.full_name}`} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('overview')}
                className={`${
                  activeTab === 'overview'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveTab('categories')}
                className={`${
                  activeTab === 'categories'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
              >
                Service Categories
              </button>
              <button
                onClick={() => setActiveTab('reports')}
                className={`${
                  activeTab === 'reports'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
              >
                Reports
              </button>
            </nav>
          </div>
        </div>

        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Categories</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalCategories}</p>
                  </div>
                  <div className="p-3 bg-blue-100 rounded-full">
                    <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Active Users</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.activeUsers}</p>
                  </div>
                  <div className="p-3 bg-green-100 rounded-full">
                    <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Requests (Today)</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.totalRequests}</p>
                  </div>
                  <div className="p-3 bg-purple-100 rounded-full">
                    <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
                  <span className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-gray-400">
                    <span className="text-base">⚡</span>
                    Fast access
                  </span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <button
                    type="button"
                    onClick={() => setActiveTab('categories')}
                    className="group relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 p-6 text-left text-white shadow-lg transition-transform hover:-translate-y-1 hover:shadow-2xl focus:outline-none focus:ring-4 focus:ring-indigo-300/60"
                  >
                    <span className="pointer-events-none absolute inset-y-0 right-0 w-32 bg-white/20 blur-3xl opacity-40" />
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="inline-flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-white/80">
                          <span className="text-lg">⭐</span>
                          Manage Categories
                        </span>
                        <p className="mt-3 text-xl font-semibold">Curate available services</p>
                        <p className="mt-2 text-sm text-white/80 max-w-xs">Create, edit, or remove service types so CSRs always see the right options.</p>
                      </div>
                      <div className="rounded-full bg-white/25 p-3 shadow-inner">
                        <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h10" />
                        </svg>
                      </div>
                    </div>
                    <div className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-white/90">
                      Open Categories
                      <svg className="h-4 w-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </button>

                  <button
                    type="button"
                    onClick={() => setActiveTab('reports')}
                    className="group relative overflow-hidden rounded-2xl bg-gradient-to-r from-orange-500 via-pink-500 to-rose-500 p-6 text-left text-white shadow-lg transition-transform hover:-translate-y-1 hover:shadow-2xl focus:outline-none focus:ring-4 focus:ring-rose-300/60"
                  >
                    <span className="pointer-events-none absolute inset-y-0 right-0 w-32 bg-white/20 blur-3xl opacity-40" />
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="inline-flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-white/80">
                          <span className="text-lg">📊</span>
                          View Reports
                        </span>
                        <p className="mt-3 text-xl font-semibold">Monitor platform health</p>
                        <p className="mt-2 text-sm text-white/80 max-w-xs">Generate daily, weekly, or monthly snapshots to keep stakeholders informed.</p>
                      </div>
                      <div className="rounded-full bg-white/25 p-3 shadow-inner">
                        <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M4 19h16M4 13h10M4 7h6" />
                        </svg>
                      </div>
                    </div>
                    <div className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-white/90">
                      Open Reports
                      <svg className="h-4 w-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </button>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">System Information</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-sm text-gray-600">Platform Version</span>
                    <span className="text-sm font-medium text-gray-900">1.0.0</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-sm text-gray-600">Last Updated</span>
                    <span className="text-sm font-medium text-gray-900">{new Date().toLocaleDateString()}</span>
                  </div>
                  <div className="flex justify-between items-center py-2">
                    <span className="text-sm text-gray-600">System Status</span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Operational
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'categories' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                <h2 className="text-xl font-bold text-gray-900">Service Categories</h2>
                <button
                  onClick={() => {
                    setCategoryForm({ service_name: '' });
                    setIsCreateModalOpen(true);
                  }}
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Add Category
                </button>
              </div>

              <div className="mb-4">
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Search categories..."
                    value={searchKeyword}
                    onChange={(e) => setSearchKeyword(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && searchCategories()}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                  <button
                    onClick={searchCategories}
                    className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition font-medium"
                  >
                    Search
                  </button>
                  {searchKeyword && (
                    <button
                      onClick={() => {
                        setSearchKeyword('');
                        fetchCategories();
                      }}
                      className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition font-medium"
                    >
                      Clear
                    </button>
                  )}
                </div>
              </div>

              {categoryError && (
                <div className="mb-4 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded">
                  {categoryError}
                </div>
              )}

              {categoriesLoading ? (
                <div className="text-center py-12">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <p className="text-gray-600 mt-2">Loading categories...</p>
                </div>
              ) : categories.length === 0 ? (
                <div className="text-center py-12">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  <p className="text-gray-600 mt-2">No categories found</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Service Name</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {categories.map((category) => (
                        <tr key={category.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{category.service_name}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-600">
                              {new Date(category.created_at).toLocaleDateString()}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                            <button
                              onClick={() => openEditModal(category)}
                              className="text-blue-600 hover:text-blue-900 mr-4"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => openDeleteModal(category)}
                              className="text-red-600 hover:text-red-900"
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Platform Reports</h2>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Report Type</label>
                  <select
                    value={reportType}
                    onChange={(e) => setReportType(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  >
                    <option value="daily">Daily Report</option>
                    <option value="weekly">Weekly Report</option>
                    <option value="monthly">Monthly Report</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {reportType === 'monthly' ? 'Month' : 'Date'}
                  </label>
                  <input
                    type={reportType === 'monthly' ? 'month' : 'date'}
                    value={reportType === 'monthly' ? reportDate.substring(0, 7) : reportDate}
                    onChange={(e) => setReportDate(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>

                <div className="flex items-end">
                  <button
                    onClick={() => fetchReport({ showToastOnSuccess: true })}
                    className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
                  >
                    Generate Report
                  </button>
                </div>
              </div>

              {reportError && (
                <div className="mb-4 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded">
                  {reportError}
                </div>
              )}

              {reportsLoading ? (
                <div className="text-center py-12">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <p className="text-gray-600 mt-2">Loading report...</p>
                </div>
              ) : reportData ? (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                      <p className="text-sm text-blue-600 font-medium">Total Requests</p>
                      <p className="text-2xl font-bold text-blue-900 mt-1">{reportData.total_requests || 0}</p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                      <p className="text-sm text-green-600 font-medium">Total Matches</p>
                      <p className="text-2xl font-bold text-green-900 mt-1">{reportData.total_matches || 0}</p>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                      <p className="text-sm text-purple-600 font-medium">New Users</p>
                      <p className="text-2xl font-bold text-purple-900 mt-1">{reportData.total_new_users || 0}</p>
                    </div>
                    <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                      <p className="text-sm text-yellow-600 font-medium">Active Users</p>
                      <p className="text-2xl font-bold text-yellow-900 mt-1">{reportData.total_active_users || 0}</p>
                    </div>
                    <div className="bg-pink-50 rounded-lg p-4 border border-pink-200">
                      <p className="text-sm text-pink-600 font-medium">Total Categories</p>
                      <p className="text-2xl font-bold text-pink-900 mt-1">{reportData.total_categories || 0}</p>
                    </div>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Report Period</h3>
                    {reportType === 'daily' && (
                      <p className="text-gray-900">{reportData.report_date}</p>
                    )}
                    {reportType === 'weekly' && (
                      <p className="text-gray-900">
                        {reportData.week_start_date} to {reportData.week_end_date}
                      </p>
                    )}
                    {reportType === 'monthly' && (
                      <p className="text-gray-900">
                        {reportData.month} ({reportData.month_start_date} to {reportData.month_end_date})
                      </p>
                    )}
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p className="text-gray-600 mt-2">Select report type and date to generate report</p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Create New Service Type</h3>
            <form onSubmit={handleCreateCategory}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Service Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g., Pet Care, Grocery Shopping"
                    value={categoryForm.service_name}
                    onChange={(e) => setCategoryForm({ ...categoryForm, service_name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>
              </div>
              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => {
                    setIsCreateModalOpen(false);
                    setCategoryForm({ service_name: '' });
                    setCategoryError('');
                  }}
                  className="flex-1 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {isEditModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Edit Service Type</h3>
            <form onSubmit={handleUpdateCategory}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Service Name</label>
                  <input
                    type="text"
                    required
                    value={categoryForm.service_name}
                    onChange={(e) => setCategoryForm({ ...categoryForm, service_name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>
              </div>
              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => {
                    setIsEditModalOpen(false);
                    setSelectedCategory(null);
                    setCategoryForm({ service_name: '' });
                    setCategoryError('');
                  }}
                  className="flex-1 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
                >
                  Update
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {isDeleteModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Delete Service Type</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete <strong>{selectedCategory?.service_name}</strong>? This action cannot be undone.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => {
                  setIsDeleteModalOpen(false);
                  setSelectedCategory(null);
                  setCategoryError('');
                }}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteCategory}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
