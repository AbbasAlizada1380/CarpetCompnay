import { useEffect, useState } from "react";
import axios from "axios";
import { MdDeleteForever } from "react-icons/md";
import { FaRegEdit } from "react-icons/fa";

const BASE_URL = import.meta.env.VITE_BASE_URL;

export default function Workers() {
  const [people, setPeople] = useState([]);
  const [formData, setFormData] = useState({
    name: "",
    father_name: "",
    permanent_residency: "",
    current_residency: "",
    nic: null,
  });
  const [editingId, setEditingId] = useState(null);
  const [refresh, setRefresh] = useState(false);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    axios.get(`${BASE_URL}/api/person/`).then((res) => setPeople(res.data));
  }, [refresh]);

  const handleInputChange = (e) => {
    const { name, value, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = new FormData();
    for (const key in formData) {
      payload.append(key, formData[key]);
    }

    try {
      if (editingId) {
        await axios.patch(`${BASE_URL}/api/person/${editingId}/`, payload);
      } else {
        await axios.post(`${BASE_URL}/api/person/`, payload);
      }
      setRefresh(!refresh);
      setFormData({
        name: "",
        father_name: "",
        permanent_residency: "",
        current_residency: "",
        nic: null,
      });
      setEditingId(null);
      setShowForm(false); // Hide form after submit
    } catch (err) {
      console.error("خطا هنگام ذخیره:", err);
    }
  };

  const handleEdit = (person) => {
    setFormData({
      name: person.name,
      father_name: person.father_name,
      permanent_residency: person.permanent_residency,
      current_residency: person.current_residency,
      nic: null,
    });
    setEditingId(person.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (confirm("آیا مطمئن هستید که می‌خواهید حذف کنید؟")) {
      await axios.delete(`${BASE_URL}/api/person/${id}/`);
      setRefresh(!refresh);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 text-right">
      <h2 className="text-2xl font-semibold mb-4">مدیریت کارگران</h2>

      <div className="mb-4 flex justify-center">
        <button
          onClick={() => {
            setShowForm(!showForm);
            setEditingId(null);
            setFormData({
              name: "",
              father_name: "",
              permanent_residency: "",
              current_residency: "",
              nic: null,
            });
          }}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          {showForm ? "بستن فورم" : "افزودن کارگر"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="space-y-4 mb-6">
          <input
            name="name"
            placeholder="نام"
            value={formData.name}
            onChange={handleInputChange}
            className="w-full p-2 border rounded"
            required
          />
          <input
            name="father_name"
            placeholder="نام پدر"
            value={formData.father_name}
            onChange={handleInputChange}
            className="w-full p-2 border rounded"
            required
          />
          <input
            name="permanent_residency"
            placeholder="سکونت دایمی"
            value={formData.permanent_residency}
            onChange={handleInputChange}
            className="w-full p-2 border rounded"
            required
          />
          <input
            name="current_residency"
            placeholder="سکونت فعلی"
            value={formData.current_residency}
            onChange={handleInputChange}
            className="w-full p-2 border rounded"
            required
          />
          <input
            type="file"
            name="nic"
            accept=".pdf,.png,.jpg"
            onChange={handleInputChange}
            className="w-full"
            required={!editingId}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            {editingId ? "ویرایش" : "ثبت"}
          </button>
        </form>
      )}

      <table className="w-full border text-right">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">#</th>
            <th className="border p-2">نام</th>
            <th className="border p-2">نام پدر</th>
            <th className="border p-2">سکونت دایمی</th>
            <th className="border p-2">سکونت فعلی</th>
            <th className="border p-2">عملیات</th>
          </tr>
        </thead>
        <tbody>
          {people.map((p, i) => (
            <tr key={p.id}>
              <td className="border p-2">{i + 1}</td>
              <td className="border p-2">{p.name}</td>
              <td className="border p-2">{p.father_name}</td>
              <td className="border p-2">{p.permanent_residency}</td>
              <td className="border p-2">{p.current_residency}</td>
              <td className="border p-2 space-x-2">
                <button
                  onClick={() => handleEdit(p)}
                  className="text-green-600 ml-2"
                  title="ویرایش"
                >
                  <FaRegEdit />
                </button>
                <button
                  onClick={() => handleDelete(p.id)}
                  className="text-red-600"
                  title="حذف"
                >
                  <MdDeleteForever />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
