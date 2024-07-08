import React, { useState } from 'react';
import styles from './App.module.css';
import { FiltersBlock } from './components/FiltersBlock/FiltersBlock';
import { Vacancy } from './components/Vacancy/Vacancy';
import { getFilteredVacancies, getMoreVacancies, getVacancies } from './utils/requests';


function App() {
    const [filtersBlock, setFiltersBlock] = useState(false);
    const [filters, setFilters] = useState({});
    const [vacancies, setVacancies] = useState();
    const [keywords, setKeywords] = useState()
    const [url, setUrl] = useState()
    const [vacanciesType, setVacanciesType] = useState()

    const [minSalary, setMinSalary] = useState()
    const [maxSalary, setMaxSalary] = useState()
    const [minExperience, setMinExperience] = useState()
    const [maxExperience, setMaxExperience] = useState()
    const [city, setCity] = useState()
    const [company, setCompany] = useState()


    async function getVacanciesData() {
      const data = await getVacancies(keywords)

      setVacancies(data.vacancies_data)
      setUrl(data.url)
      setVacanciesType('simple')
    }

    async function getMoreVacanciesData() {
      console.log('click')
      const data = await getMoreVacancies(url)

      setVacancies(data.vacancies_data)
      setUrl(data.url)
      setVacanciesType('simple')
    }
    

    function handleVacancies(vacancies) {
      setVacancies(vacancies)
    }

    function handleUrl(url) {
      setUrl(url)
    }

    function handleType(type) {
      setVacanciesType(type)
    }
 
    console.log(vacanciesType)
  
    return (
        <div className={styles.app}>
            <div className={styles.searchSection}>
                <p className={styles.searchTitle}>Введите ключевые слова для поиска вакансии</p>
                <input className={styles.searchInput} placeholder='Ключевые слова' onChange={(event) => setKeywords(event.target.value)}/>
                <div className={styles.buttonsSection}>
                  <span className={styles.button} onClick={() => getVacanciesData()}>
                    Найти
                  </span>
                  {
                    vacanciesType == 'simple' &&
                    <button  className={vacanciesType == 'simple' ? styles.button : styles.disabledButton } onClick={() => getMoreVacanciesData()}>
                    Найти больше
                  </button>
                  }
                  

                  
                </div>
                <span 
                      className={styles.advancedSearch}
                      onClick={() => setFiltersBlock(!filtersBlock)}
                  >
                      Расширенный поиск
                  </span>
                
                {filtersBlock && <FiltersBlock handleVacancies={handleVacancies} handleUrl={handleUrl} keywords={keywords} url={url} handleType={handleType} type={vacanciesType} />}
            </div>

            

            <div className={styles.vacanciesSection}>
                <div className={styles.titlesSection}>
                  <h2 className={styles.vacanciesTitle}>Найденные вакансии</h2>
                </div>
                <div className={styles.vacanciesList}>

                    {vacancies ? (
                        vacancies.map((vacancy, index) => {
                          console.log(vacancy)
                          return (
                            <Vacancy key={index} city={vacancy.city} name={vacancy.name} text={vacancy.salary.text} experience={vacancy.experience_text} company={vacancy.company} />)
})
                    ) : (
                        <p className={styles.noVacancies}>Вакансии не найдены</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default App;
