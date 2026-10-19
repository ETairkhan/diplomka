package models

type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
	Role  string `json:"role"` // system_admin, org_admin, teacher, student, parent
}
