
export async function getVacancies(keywords){
    const response = await fetch(
        `http://127.0.0.1:8000/get_vacancies_by_key_words`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "keywords": keywords
          })
        }
      );
      
      const data = await response.json();
      return data
}


export async function getMoreVacancies(url){
    const response = await fetch(
        `http://127.0.0.1:8000/get_more_vacancies`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "url": url
          })
        }
      );
      
      const data = await response.json();
      return data
}


export async function getFilteredVacancies(salaryRange, experienceRange, city, company, keywords ){
    const response = await fetch(
        `http://127.0.0.1:8000/get_filtered_vacancies`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "salary_range":  salaryRange,
            "experience_range": experienceRange,
            "city": city,
            "company": company,
            "keywords": keywords
          })
        }
      );
      
      const data = await response.json();
      return data
}

export async function getMoreFilteredVacancies(salaryRange = null, experienceRange = null, city = null, company = null, url = null) {
    const response = await fetch(
        `http://127.0.0.1:8000/get_more_filtered_vacancies`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "salary_range":  salaryRange,
            "experience_range": experienceRange,
            "city": city,
            "company": company,
            "url": url
          })
        }
      );
      
      const data = await response.json();
      return data
}