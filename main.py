from app import create_app


if __name__ == "__main__":
    app = create_app()
    # print(app.url_map)

    # execute app
    app.run(host="localhost", port="1234", debug=True)