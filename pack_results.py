import os
import sys
import zipfile
import logging
from pathlib import Path
from datetime import datetime

def setup_logging(output_dir):
    """设置日志记录"""
    log_file = output_dir / f"pack_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_file

def create_zip_from_folder(source_folder, zip_path):
    """
    将源文件夹的内容直接打包到ZIP文件中（不包含文件夹结构）
    
    参数:
        source_folder: 要打包的源文件夹路径
        zip_path: 生成的ZIP文件路径
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in source_folder.iterdir():
            # 将文件直接添加到ZIP根目录，不保留路径结构
            zipf.write(item, item.name)

def main():
    """主函数"""
    print("\n" + "="*50)
    print("    Result文件夹批量打包工具")
    print("="*50 + "\n")
    
    # 获取当前工作目录
    current_dir = Path.cwd()
    print(f"当前工作目录：{current_dir}")
    print()
    
    # 创建输出目录
    output_dir = current_dir / "zip_output"
    output_dir.mkdir(exist_ok=True)
    print(f"输出目录：{output_dir}")
    print()
    
    # 设置日志
    log_file = setup_logging(output_dir)
    logging.info(f"开始打包操作 - 工作目录: {current_dir}, 输出目录: {output_dir}")
    
    print("="*50)
    print("          开始处理文件夹")
    print("="*50)
    print()
    
    # 计数器
    total_folders_checked = 0
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    # 遍历当前目录下的所有子文件夹
    for item in current_dir.iterdir():
        if item.is_dir() and item.name != "zip_output":
            total_folders_checked += 1
            folder_name = item.name
            
            print("-" * 50)
            print(f"正在检查文件夹: {folder_name}")
            
            # 检查是否存在result文件夹
            result_folder = item / "result"
            if result_folder.exists() and result_folder.is_dir():
                print("  -> 找到result文件夹，准备打包...")
                
                # 检查result文件夹是否为空
                if not any(result_folder.iterdir()):
                    print("  -> [跳过] result文件夹为空")
                    skipped_count += 1
                    logging.info(f"[跳过] {folder_name} - result文件夹为空")
                    continue
                
                # 创建ZIP文件路径
                zip_file_path = output_dir / f"{folder_name}.zip"
                
                try:
                    # 打包result文件夹内容
                    print(f"  -> 正在压缩: {zip_file_path}")
                    create_zip_from_folder(result_folder, zip_file_path)
                    
                    print(f"  -> [成功] 打包完成: {folder_name}.zip")
                    success_count += 1
                    logging.info(f"[成功] {folder_name} - 打包完成")
                    
                except Exception as e:
                    print(f"  -> [失败] 打包文件夹时出错: {e}")
                    error_count += 1
                    logging.error(f"[失败] {folder_name} - 打包错误: {e}")
            else:
                print("  -> [跳过] 未找到result文件夹")
                skipped_count += 1
                logging.info(f"[跳过] {folder_name} - 未找到result文件夹")
            
            print()
    
    # 显示统计结果
    print("-" * 50)
    print()
    print("=" * 50)
    print("          处理完成统计")
    print("=" * 50)
    print(f"总共检查文件夹数: {total_folders_checked}")
    print(f"成功打包: {success_count}个")
    print(f"失败: {error_count}个")
    print(f"跳过: {skipped_count}个")
    print()
    print(f"输出目录: {output_dir}")
    print(f"日志文件: {log_file}")
    print()
    
    # 记录统计结果到日志
    logging.info("===== 打包完成统计 =====")
    logging.info(f"总共检查文件夹数: {total_folders_checked}")
    logging.info(f"成功打包: {success_count}个")
    logging.info(f"失败: {error_count}个")
    logging.info(f"跳过: {skipped_count}个")
    
    # 统计结果提示
    if total_folders_checked == 0:
        print()
        print("注意：当前目录下没有找到任何子文件夹。")
        print("请确保您在包含项目子文件夹的父目录中运行此脚本。")
    else:
        if success_count > 0:
            print()
            print(f"处理完成！成功打包了 {success_count} 个文件夹的result内容。")
        else:
            print()
            print(f"注意：已检查 {total_folders_checked} 个文件夹，但均未找到名为 result 的子文件夹。")
            print("请确保：")
            print("1. 您在正确的父目录中运行此脚本。")
            print("2. 目标子文件夹中确实存在名为 result 的文件夹。")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生未预期错误: {e}")
        sys.exit(1)
    
    # 等待用户按键（仅Windows）
    if os.name == 'nt':
        input("按Enter键退出...")