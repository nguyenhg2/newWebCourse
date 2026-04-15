import Hero from "../components/Hero";
import Categories from "../components/Categories";
import CourseList from "../components/CourseList";
import Stats from "../components/Stats";
import Benefits from "../components/Benefits";
import Testimonials from "../components/Testimonials";
import BlogSection from "../components/BlogSection";

export default function Home() {
  return (
    <>
      <Hero />
      <Categories />
      <CourseList />
      <Stats />
      <Benefits />
      <Testimonials />
      <BlogSection />
    </>
  );
}
