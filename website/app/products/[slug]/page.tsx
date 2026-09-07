import { notFound } from 'next/navigation';
import products from '@/app/products-data.json';
import ProductWorkspace from '@/components/products/ProductWorkspace';
export function generateStaticParams() {
  return products.map((p) => ({ slug: p.slug }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const p = products.find((x) => x.slug === slug);
  return {
    title: p ? `${p.short} — AI Braking Engineering` : 'Product not found',
  };
}
export default async function ProductPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const p = products.find((x) => x.slug === slug);
  if (!p) notFound();
  return <ProductWorkspace product={p} />;
}
