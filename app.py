from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        try:
            marks = [float(request.form.get(f"mark{i}", 0)) for i in range(1, 6)]
            credits = [float(request.form.get(f"credit{i}", 0)) for i in range(1, 6)]

            if any(m < 0 or m > 100 for m in marks):
                raise ValueError("Marks must be between 0 and 100.")
            if any(c <= 0 for c in credits):
                raise ValueError("Credits must be greater than 0.")

            # Example grade-point mapping; change it to your university rules if needed.
            grade_points = []
            for m in marks:
                if m >= 90:
                    gp = 10
                elif m >= 80:
                    gp = 9
                elif m >= 70:
                    gp = 8
                elif m >= 60:
                    gp = 7
                elif m >= 50:
                    gp = 6
                elif m >= 40:
                    gp = 5
                else:
                    gp = 0
                grade_points.append(gp)

            total_credits = sum(credits)
            cgpa = sum(g * c for g, c in zip(grade_points, credits)) / total_credits
            percentage = cgpa * 10  # Common conversion; verify your university's rule.

            result = {
                "cgpa": round(cgpa, 2),
                "percentage": round(percentage, 2)
            }

        except ValueError as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
