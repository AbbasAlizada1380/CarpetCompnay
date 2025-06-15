import { useEffect, useState } from "react";
import axios from "axios";
import { MdDeleteForever } from "react-icons/md";
import { FaRegEdit } from "react-icons/fa";

const BASE_URL = import.meta.env.VITE_BASE_URL;

export default function Importing() {
  const [carpets, setCarpets] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    source: "",
    description: "",
    quality: "",
    length: "",
    width: "",
    rate: "",
    weight: "",
  });
  const [editingId, setEditingId] = useState(null);

  const fetchCarpets = async () => {
    const res = await axios.get(`${BASE_URL}/carpet/carpets/`);
    setCarpets(res.data);
  };

  useEffect(() => {
    fetchCarpets();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const dataToSend = {
      ...formData,
      length: parseFloat(formData.length),
      width: parseFloat(formData.width),
      rate: parseFloat(formData.rate),
      price: 0,
    };

    if (editingId) {
      await axios.patch(`${BASE_URL}/carpet/carpets/${editingId}/`, dataToSend);
    } else {
      await axios.post(`${BASE_URL}/carpet/carpets/`, dataToSend);
    }

    setFormData({
      source: "",
      description: "",
      quality: "",
      length: "",
      width: "",
      rate: "",
      weight: "",
    });
    setEditingId(null);
    setShowForm(false);
    fetchCarpets();
  };

  const handleEdit = (carpet) => {
    setFormData({
      source: carpet.source,
      description: carpet.description,
      quality: carpet.quality,
      length: carpet.length,
      width: carpet.width,
      rate: carpet.rate,
      weight: carpet.weight,
    });
    setEditingId(carpet.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    await axios.delete(`${BASE_URL}/carpet/carpets/${id}/`);
    fetchCarpets();
  };

  const labels = {
    source: "مبدأ",
    description: "توضیحات",
    quality: "کیفیت",
    length: "طول",
    width: "عرض",
    rate: "نرخ",
    weight: "وزن",
    degree: "درجه",
  };

  return (
    <div
      className="p-6 font-sans bg-white rounded-lg shadow-lg max-w-6xl mx-auto"
      dir="rtl"
    >
      <h2 className="text-2xl font-bold mb-6 text-right text-gray-800 border-b pb-2">
        واردات قالین
      </h2>
      {/* Toggle Button */}
      {!showForm && (
        <div className="flex justify-center items-center mb-4">
          <button
            onClick={() => {
              setShowForm(true);
              setEditingId(null);
              setFormData({
                source: "",
                description: "",
                quality: "",
                length: "",
                width: "",
                rate: "",
                weight: "",
              });
            }}
            className={` mb-4 bg-green-500 text-white p-2 rounded`} // MATCHING OTHER STYLES
          >
            اضافه کردن قالین جدید
          </button>
        </div>
      )}

      {/* Form Section */}
      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-gray-200 max-w-5xl mx-auto p-10 shadow rounded mb-4" // MATCHING STYLE
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {Object.entries(labels).map(([field, label]) => (
              <div key={field} className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  {label}:
                </label>
                {field === "source" ? (
                  <select
                    name="source"
                    value={formData.source}
                    onChange={handleChange}
                    required
                    className="shadow appearance-none border bg-white rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-right"
                  >
                    <option value="">انتخاب کنید</option>
                    <option value="حاجی تقی">حاجی تقی</option>
                    <option value="جعفر">جعفر</option>
                    <option value="اسحاق">اسحاق</option>
                  </select>
                ) : (
                  <input
                    name={field}
                    value={formData[field]}
                    onChange={handleChange}
                    placeholder={label}
                    required
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 bg-white leading-tight focus:outline-none focus:shadow-outline text-right"
                  />
                )}
              </div>
            ))}
          </div>

          {/* Form Buttons */}
          <div className="flex items-center justify-center gap-5 mt-4">
            <button
              type="submit"
              className="bg-green-500 text-white py-2 px-7 rounded-md cursor-pointer hover:bg-green-700 transition-all"
            >
              {editingId ? "ویرایش" : "ثبت"}
            </button>
            <button
              onClick={() => setShowForm(false)}
              type="button"
              className="bg-red-600 text-white hover:bg-red-700 cursor-pointer py-2 px-4 rounded-md"
            >
              انصراف
            </button>
          </div>
        </form>
      )}

      <div className="overflow-x-auto">
        <table className="min-w-full leading-normal border border-gray-300 text-sm">
          <thead>
            <tr className="bg-primary text-white text-md font-semibold uppercase tracking-wider">
              <th className="border border-gray-300 py-3 px-4">مبدأ</th>
              <th className="border border-gray-300 py-3 px-4">توضیحات</th>
              <th className="border border-gray-300 py-3 px-4">کیفیت</th>
              <th className="border border-gray-300 py-3 px-4">طول</th>
              <th className="border border-gray-300 py-3 px-4">عرض</th>
              <th className="border border-gray-300 py-3 px-4">نرخ</th>
              <th className="border border-gray-300 py-3 px-4">قیمت</th>
              <th className="border border-gray-300 py-3 px-4">وزن</th>
              <th className="border border-gray-300 py-3 px-4">درجه</th>
              <th className="border border-gray-300 py-3 px-4">عملیات</th>
            </tr>
          </thead>
          <tbody>
            {carpets.map((carpet) => (
              <tr
                key={carpet.id}
                className="border-b border-gray-300 text-center hover:bg-gray-100 transition-colors duration-300"
              >
                <td className="py-3 px-4">{carpet.source}</td>
                <td className="py-3 px-4">{carpet.description}</td>
                <td className="py-3 px-4">{carpet.quality}</td>
                <td className="py-3 px-4">{carpet.length}</td>
                <td className="py-3 px-4">{carpet.width}</td>
                <td className="py-3 px-4">{carpet.rate}</td>
                <td className="py-3 px-4">{carpet.price}</td>
                <td className="py-3 px-4">{carpet.weight}</td>
                <td className="py-3 px-4">{carpet.weight}</td>
                <td className="py-3 px-4">
                  <div className="flex justify-center items-center gap-3">
                    <button
                      onClick={() => handleEdit(carpet)}
                      className="text-blue-600 hover:text-blue-800 transition-all duration-300 transform hover:scale-110"
                      title="ویرایش"
                    >
                      <FaRegEdit size={20} />
                    </button>
                    <button
                      onClick={() => handleDelete(carpet.id)}
                      className="text-red-600 hover:text-red-800 transition-all duration-300 transform hover:scale-110"
                      title="حذف"
                    >
                      <MdDeleteForever size={24} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {carpets.length === 0 && (
              <tr>
                <td colSpan="9" className="text-center py-6 text-gray-500">
                  هیچ لیستی ثبت نشده است.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
