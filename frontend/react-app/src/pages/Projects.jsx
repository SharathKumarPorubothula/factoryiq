import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Projects.css";

const API_URL = "http://localhost/api/api";

const PAGE_SIZE = 5;

function Projects() {
  const navigate = useNavigate();

  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Search
  const [search, setSearch] = useState("");

  // Filters
  const [filters, setFilters] = useState({
    customer: "",
    site: "",
    program: "",
    status: "",
    health: "",
    owner: "",
    date: "",
  });

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      setError("");

      const token = localStorage.getItem("access_token");

      const response = await fetch(`${API_URL}/project`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",

          ...(token
            ? {
                Authorization: `Bearer ${token}`,
              }
            : {}),
        },
      });

      const data = await response.json();

      console.log("Projects API response:", data);

      if (!response.ok) {
        throw new Error(
          data.error || `Failed to load projects (${response.status})`
        );
      }

      setProjects(data.projects || []);
    } catch (err) {
      console.error("Failed to load projects:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // Helpers
  // ============================================================

  const formatDate = (date) => {
    if (!date) return "-";

    return new Date(date).toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  };

  const getOwner = (project) => {
    if (!project.members || project.members.length === 0) {
      return "-";
    }

    const projectManager = project.members.find(
      (member) => member.role === "Project Manager"
    );

    if (projectManager?.user) {
      return (
        projectManager.user.first_name ||
        projectManager.user.username ||
        "-"
      );
    }

    return projectManager?.user_id
      ? projectManager.user_id.substring(0, 8)
      : "-";
  };

  /*
   * Your current API response does not contain explicit
   * customer/site fields or health fields.
   *
   * These are therefore displayed as "-" until those
   * fields are returned by the backend.
   */

  const getCustomer = (project) => {
    return project.customer || "-";
  };

  const getSite = (project) => {
    return project.site || "-";
  };

  const getHealth = (project) => {
    if (project.health) {
      return project.health.toUpperCase();
    }

    // Calculate a simple health from current project data.
    if (project.status === "delayed") {
      return "RED";
    }

    const criticalRisk = project.risks?.some(
      (risk) =>
        risk.impact === "critical" ||
        risk.probability === "critical"
    );

    if (criticalRisk) {
      return "RED";
    }

    const highRisk = project.risks?.some(
      (risk) =>
        risk.impact === "high" ||
        risk.probability === "high"
    );

    if (highRisk) {
      return "AMBER";
    }

    if (project.status === "active") {
      return "GREEN";
    }

    return "-";
  };

  // ============================================================
  // Filter options
  // ============================================================

  const customerOptions = useMemo(() => {
    return [
      ...new Set(
        projects
          .map((project) => getCustomer(project))
          .filter((value) => value !== "-")
      ),
    ];
  }, [projects]);

  const siteOptions = useMemo(() => {
    return [
      ...new Set(
        projects
          .map((project) => getSite(project))
          .filter((value) => value !== "-")
      ),
    ];
  }, [projects]);

  const programOptions = useMemo(() => {
    return [
      ...new Set(
        projects
          .map((project) => project.program?.name)
          .filter(Boolean)
      ),
    ];
  }, [projects]);

  const ownerOptions = useMemo(() => {
    return [
      ...new Set(
        projects
          .map((project) => getOwner(project))
          .filter((value) => value !== "-")
      ),
    ];
  }, [projects]);

  // ============================================================
  // Search + Filtering
  // ============================================================

  const filteredProjects = useMemo(() => {
    const searchValue = search.trim().toLowerCase();

    return projects.filter((project) => {
      const customer = getCustomer(project);
      const site = getSite(project);
      const program = project.program?.name || "";
      const owner = getOwner(project);
      const health = getHealth(project);

      // Search
      const matchesSearch =
        !searchValue ||
        project.project_code
          ?.toLowerCase()
          .includes(searchValue) ||
        project.name
          ?.toLowerCase()
          .includes(searchValue) ||
        project.description
          ?.toLowerCase()
          .includes(searchValue) ||
        customer.toLowerCase().includes(searchValue) ||
        site.toLowerCase().includes(searchValue) ||
        program.toLowerCase().includes(searchValue) ||
        owner.toLowerCase().includes(searchValue);

      if (!matchesSearch) {
        return false;
      }

      // Customer
      if (
        filters.customer &&
        customer !== filters.customer
      ) {
        return false;
      }

      // Site
      if (
        filters.site &&
        site !== filters.site
      ) {
        return false;
      }

      // Program
      if (
        filters.program &&
        program !== filters.program
      ) {
        return false;
      }

      // Status
      if (
        filters.status &&
        project.status !== filters.status
      ) {
        return false;
      }

      // Health
      if (
        filters.health &&
        health !== filters.health
      ) {
        return false;
      }

      // Owner
      if (
        filters.owner &&
        owner !== filters.owner
      ) {
        return false;
      }

      return true;
    });
  }, [projects, search, filters]);

  // ============================================================
  // Pagination
  // ============================================================

  const totalPages = Math.max(
    1,
    Math.ceil(filteredProjects.length / PAGE_SIZE)
  );

  const paginatedProjects = filteredProjects.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE
  );

  const startItem =
    filteredProjects.length === 0
      ? 0
      : (currentPage - 1) * PAGE_SIZE + 1;

  const endItem = Math.min(
    currentPage * PAGE_SIZE,
    filteredProjects.length
  );

  // ============================================================
  // Search / Filter handlers
  // ============================================================

  const handleSearch = (event) => {
    setSearch(event.target.value);
    setCurrentPage(1);
  };

  const handleFilterChange = (name, value) => {
    setFilters((previous) => ({
      ...previous,
      [name]: value,
    }));

    setCurrentPage(1);
  };

  const clearFilters = () => {
    setSearch("");

    setFilters({
      customer: "",
      site: "",
      program: "",
      status: "",
      health: "",
      owner: "",
      date: "",
    });

    setCurrentPage(1);
  };

  // ============================================================
  // Pagination handlers
  // ============================================================

  const goToPage = (page) => {
    if (page < 1 || page > totalPages) {
      return;
    }

    setCurrentPage(page);
  };

  // ============================================================
  // Loading
  // ============================================================

  if (loading) {
    return (
      <div className="projects-page">
        <div className="loading">
          Loading projects...
        </div>
      </div>
    );
  }

  // ============================================================
  // Error
  // ============================================================

  if (error) {
    return (
      <div className="projects-page">
        <div className="error-box">
          <h3>Unable to load projects</h3>

          <p>{error}</p>

          <button onClick={loadProjects}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  // ============================================================
  // Page
  // ============================================================

  return (
    <div className="projects-page">

      {/* ====================================================== */}
      {/* HEADER                                                 */}
      {/* ====================================================== */}

      <div className="projects-header">

        <div>
          <h1>Projects</h1>

          <p>
            Manage and track all projects
          </p>
        </div>

        <button
          className="create-project-btn"
          onClick={() =>
            navigate("/projects/create")
          }
        >
          [+ Create Project]
        </button>

      </div>

      {/* ====================================================== */}
      {/* SEARCH                                                 */}
      {/* ====================================================== */}

      <div className="search-section">

        <input
          type="text"
          className="project-search"
          placeholder="Search projects..."
          value={search}
          onChange={handleSearch}
        />

      </div>

      {/* ====================================================== */}
      {/* FILTERS                                                */}
      {/* ====================================================== */}

      <div className="filter-section">

        <select
          value={filters.customer}
          onChange={(e) =>
            handleFilterChange(
              "customer",
              e.target.value
            )
          }
        >
          <option value="">Customer ▼</option>

          {customerOptions.map((customer) => (
            <option
              key={customer}
              value={customer}
            >
              {customer}
            </option>
          ))}
        </select>

        <select
          value={filters.site}
          onChange={(e) =>
            handleFilterChange(
              "site",
              e.target.value
            )
          }
        >
          <option value="">Site ▼</option>

          {siteOptions.map((site) => (
            <option
              key={site}
              value={site}
            >
              {site}
            </option>
          ))}
        </select>

        <select
          value={filters.program}
          onChange={(e) =>
            handleFilterChange(
              "program",
              e.target.value
            )
          }
        >
          <option value="">Program ▼</option>

          {programOptions.map((program) => (
            <option
              key={program}
              value={program}
            >
              {program}
            </option>
          ))}
        </select>

        <select
          value={filters.status}
          onChange={(e) =>
            handleFilterChange(
              "status",
              e.target.value
            )
          }
        >
          <option value="">Status ▼</option>
          <option value="active">Active</option>
          <option value="delayed">Delayed</option>
          <option value="planning">Planning</option>
          <option value="draft">Draft</option>
        </select>

        <select
          value={filters.health}
          onChange={(e) =>
            handleFilterChange(
              "health",
              e.target.value
            )
          }
        >
          <option value="">Health ▼</option>
          <option value="GREEN">GREEN</option>
          <option value="AMBER">AMBER</option>
          <option value="RED">RED</option>
        </select>

        <select
          value={filters.owner}
          onChange={(e) =>
            handleFilterChange(
              "owner",
              e.target.value
            )
          }
        >
          <option value="">Owner ▼</option>

          {ownerOptions.map((owner) => (
            <option
              key={owner}
              value={owner}
            >
              {owner}
            </option>
          ))}
        </select>

        <select
          value={filters.date}
          onChange={(e) =>
            handleFilterChange(
              "date",
              e.target.value
            )
          }
        >
          <option value="">Date ▼</option>
          <option value="newest">
            Newest
          </option>
          <option value="oldest">
            Oldest
          </option>
        </select>

        {(search ||
          Object.values(filters).some(Boolean)) && (
          <button
            className="clear-filter-btn"
            onClick={clearFilters}
          >
            Clear
          </button>
        )}

      </div>

      {/* ====================================================== */}
      {/* TABLE                                                  */}
      {/* ====================================================== */}

      <div className="projects-card">

        <div className="table-container">

          <table>

            <thead>

              <tr>

                <th>Project</th>
                <th>Name</th>
                <th>Customer</th>
                <th>Site</th>
                <th>Program</th>
                <th>Owner</th>
                <th>Status</th>
                <th>Health</th>

              </tr>

            </thead>

            <tbody>

              {paginatedProjects.length === 0 ? (

                <tr>

                  <td
                    colSpan="8"
                    className="no-projects"
                  >
                    No projects found
                  </td>

                </tr>

              ) : (

                paginatedProjects.map((project) => {

                  const health =
                    getHealth(project);

                  return (

                    <tr
                      key={project.id}
                      className="project-row"
                      onClick={() =>
                        navigate(
                          `/projects/${project.id}/audit`
                        )
                      }
                    >

                      {/* Project Code */}

                      <td>
                        <span className="project-code">
                          {project.project_code}
                        </span>
                      </td>

                      {/* Name */}

                      <td>

                        <div className="project-name">
                          {project.name}
                        </div>

                      </td>

                      {/* Customer */}

                      <td>
                        {getCustomer(project)}
                      </td>

                      {/* Site */}

                      <td>
                        {getSite(project)}
                      </td>

                      {/* Program */}

                      <td>
                        {project.program?.name || "-"}
                      </td>

                      {/* Owner */}

                      <td>
                        {getOwner(project)}
                      </td>

                      {/* Status */}

                      <td>

                        <span
                          className={`status status-${project.status}`}
                        >
                          {project.status}
                        </span>

                      </td>

                      {/* Health */}

                      <td>

                        {health === "GREEN" && (
                          <span className="health green">
                            GREEN
                          </span>
                        )}

                        {health === "AMBER" && (
                          <span className="health amber">
                            AMBER
                          </span>
                        )}

                        {health === "RED" && (
                          <span className="health red">
                            RED
                          </span>
                        )}

                        {health === "-" && (
                          <span className="health">
                            -
                          </span>
                        )}

                      </td>

                    </tr>

                  );
                })

              )}

            </tbody>

          </table>

        </div>

        {/* ==================================================== */}
        {/* PAGINATION                                           */}
        {/* ==================================================== */}

        <div className="pagination">

          <div className="pagination-info">

            Showing{" "}
            <strong>{startItem}</strong>
            {" - "}
            <strong>{endItem}</strong>
            {" of "}
            <strong>
              {filteredProjects.length}
            </strong>

          </div>

          <div className="pagination-controls">

            <button
              className="page-arrow"
              disabled={currentPage === 1}
              onClick={() =>
                goToPage(currentPage - 1)
              }
            >
              ◀
            </button>

            {Array.from(
              { length: totalPages },
              (_, index) => index + 1
            ).map((page) => (

              <button
                key={page}
                className={
                  currentPage === page
                    ? "page-number active"
                    : "page-number"
                }
                onClick={() =>
                  goToPage(page)
                }
              >
                {page}
              </button>

            ))}

            <button
              className="page-arrow"
              disabled={
                currentPage === totalPages
              }
              onClick={() =>
                goToPage(currentPage + 1)
              }
            >
              ▶
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Projects;