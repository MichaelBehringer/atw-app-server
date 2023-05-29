package models

type Person struct {
	PersNo    int    `json:"persNo"`
	Lastname  string `json:"lastname"`
	Firstname string `json:"firstname"`
}

type YearCityResult struct {
	Lastname        string `json:"lastname"`
	FlaschenFuellen int    `json:"flaschenFuellen"`
	FlaschenTuev    int    `json:"flaschenTuev"`
	MaskenPruefen   int    `json:"maskenPruefen"`
	MaskenReinigen  int    `json:"maskenReinigen"`
	LaPruefen       int    `json:"laPruefen"`
	LaReinigen      int    `json:"laReinigen"`
	GeraetePruefen  int    `json:"geraetePruefen"`
	GeraeteReinigen int    `json:"geraeteReinigen"`
	DateWork        string `json:"dateWork"`
}
