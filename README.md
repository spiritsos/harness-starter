# Order Service

주문 관리 API 서버입니다.

## 실행

```
pip install -r requirements.txt
python scripts/seed.py
uvicorn app.main:app --reload
```

http://127.0.0.1:8000/docs 에서 API를 확인할 수 있습니다.
