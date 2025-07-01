from datetime import datetime

import httpx
import streamlit as st
from pydantic import BaseModel, Field  # Pydantic BaseModelをインポート

# APIのベースURL
API_BASE_URL = "http://localhost:8000"


# APIのProductModelと一致するよう定義
class ProductCreate(BaseModel):
    """商品作成リクエストモデル"""

    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)


class ProductResponse(BaseModel):
    """商品レスポンスモデル"""

    id: int
    name: str
    price: float
    created_at: datetime


def check_api_status() -> bool:
    """APIのヘルスチェックを行い、稼働状態を返します。"""
    try:
        response = httpx.get(f"{API_BASE_URL}/health")
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        return True
    except httpx.RequestError:
        st.error("APIサーバーに接続できません。FastAPIサーバーが起動しているか確認してください。")
        return False
    except httpx.HTTPStatusError as e:
        st.error(f"APIエラーが発生しました: HTTP {e.response.status_code} - {e.response.text}")
        return False


def main() -> None:
    """Streamlit 商品管理UIのメイン関数"""
    st.set_page_config(page_title="商品管理UI", layout="centered")
    st.title("🛒 商品管理UI")
    st.markdown("---")

    # APIステータス表示
    st.sidebar.subheader("APIサーバーのステータス")
    if check_api_status():
        st.sidebar.success("APIサーバーはオンラインです ✅")
    else:
        st.sidebar.error("APIサーバーはオフラインです ❌")
        st.sidebar.info(
            (
                "別のターミナルで `cd api && uv run uvicorn main:app --reload` を"
                "実行してAPIを起動してください。"
            )
        )
        return  # APIが起動していない場合はこれ以上進まない

    st.subheader("💰 新しい商品を登録する")
    with st.form(key="product_registration_form"):
        product_name = st.text_input("商品名", key="reg_product_name")
        product_price = st.number_input(
            "価格 (0より大きい値を入力してください)",
            min_value=0.01,
            format="%.2f",
            key="reg_product_price",
        )
        submit_button = st.form_submit_button(label="商品登録")

        if submit_button:
            if not product_name:
                st.error("⚠️ 商品名は必須項目です。入力してください。")
            elif product_price <= 0:
                st.error("⚠️ 価格は0より大きい数値を入力してください。")
            else:
                try:
                    new_product_data = ProductCreate(
                        name=product_name, price=product_price
                    ).model_dump_json()
                    response = httpx.post(
                        f"{API_BASE_URL}/items",
                        content=new_product_data,
                        headers={"Content-Type": "application/json"},
                    )
                    response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
                    registered_product = ProductResponse(**response.json())
                    st.success("🎉 商品が正常に登録されました！")
                    st.write("**登録された商品詳細:**")
                    st.json(registered_product.model_dump())
                    st.info(
                        "新しい商品を続けて登録するには、画面を更新（ブラウザのリロード）してください。"
                    )  # フォームをクリアするために再実行を促す（Streamlitの制限）
                except httpx.RequestError as e:
                    st.error(f"❌ APIへのリクエストに失敗しました: {e}")
                except httpx.HTTPStatusError as e:
                    error_detail = e.response.json().get("detail", "不明なエラー")
                    st.error(
                        f"❌ 商品登録に失敗しました: "
                        f"HTTPエラー {e.response.status_code} - {error_detail}"
                    )
                except Exception as e:
                    st.error(f"🚨 予期せぬエラーが発生しました: {e}")

    st.markdown("--- ")

    st.subheader("🔍 商品をIDで検索する")
    with st.form(key="product_search_form"):
        item_id_input = st.number_input(
            "検索する商品IDを入力してください", min_value=1, format="%d", key="search_item_id"
        )
        search_button = st.form_submit_button(label="商品検索")

        if search_button:
            if item_id_input <= 0:
                st.error("⚠️ 商品IDは1以上の整数を入力してください。")
            else:
                try:
                    response = httpx.get(f"{API_BASE_URL}/items/{int(item_id_input)}")
                    response.raise_for_status()
                    found_product = ProductResponse(**response.json())
                    st.success("✨ 商品が見つかりました！")
                    st.write("**検索された商品詳細:**")
                    st.json(found_product.model_dump())
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        st.warning(
                            f"🔍 指定されたID ({int(item_id_input)}) の商品は見つかりませんでした。"
                        )
                    else:
                        error_detail = e.response.json().get("detail", "不明なエラー")
                        st.error(
                            f"❌ 商品検索に失敗しました: "
                            f"HTTPエラー {e.response.status_code} - {error_detail}"
                        )
                except httpx.RequestError as e:
                    st.error(f"❌ APIへのリクエストに失敗しました: {e}")
                except Exception as e:
                    st.error(f"🚨 予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
