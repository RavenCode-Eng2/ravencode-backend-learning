// Example of how to modify your Courses component to use the API

import React, { useState, useEffect } from "react";
import Button from "../components/Button";
import { theme } from "../theme";
import python_logo from "../assets/images/python_logo.png";
import flujo_logo from "../assets/images/flujo_logo.png";
import { Link } from 'react-router-dom';
import { useAuth } from "../context/AuthContext";
import { learningService } from "../services/learningService";

// Add this to your learningService or create a new courseService
const courseService = {
  async getCourses() {
    try {
      const response = await fetch('http://localhost:8002/courses/frontend-data');
      if (!response.ok) {
        throw new Error('Failed to fetch courses');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching courses:', error);
      // Fallback to mock data endpoint if main endpoint fails
      try {
        const mockResponse = await fetch('http://localhost:8002/courses/frontend-data/mock');
        return await mockResponse.json();
      } catch (mockError) {
        console.error('Error fetching mock courses:', mockError);
        return [];
      }
    }
  }
};

const Courses = () => {
  const { user } = useAuth();
  const [courseData, setCourseData] = useState([]);
  const [module2Unlocked, setModule2Unlocked] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const courses = await courseService.getCourses();
        setCourseData(courses);
      } catch (error) {
        console.error('Error loading courses:', error);
      }
    };

    fetchCourses();
  }, []);

  useEffect(() => {
    const checkModule1Passed = async () => {
      if (!user) {
        setModule2Unlocked(false);
        setLoading(false);
        return;
      }
      try {
        const res = await learningService.getGrade(user.correo_electronico, "Assessment1");
        console.log("Respuesta del backend:", res);
        console.log("Grade recibido:", res.data?.grade);
        setModule2Unlocked(res.data?.grade >= 40);
      } catch (e) {
        setModule2Unlocked(false);
      }
      setLoading(false);
    };
    checkModule1Passed();
  }, [user]);

  if (loading) return <div className="text-white">Cargando...</div>;

  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <div className="flex flex-wrap justify-between gap-3 p-4">
          <div className="flex min-w-72 flex-col gap-3">
            <p className="text-white tracking-light text-[32px] font-bold leading-tight">
              Cursos disponibles
            </p>
            <p className="text-[#9caaba] text-sm font-normal leading-normal">
              Explora nuestra lista de cursos de programación diseñados para aprender desde cero. ¡Comienza tu viaje de programación hoy!
            </p>
          </div>
        </div>
        
        {courseData.map((course) => (
          <CourseCard
            key={course.id}
            course={course}
            module2Unlocked={module2Unlocked}
          />
        ))}
      </div>
    </div>
  );
};

// Rest of your component code remains the same...
// ModuleCard, CourseCard components stay unchanged

export default Courses; 